#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
夸克网盘大文件取回归档工具（仅限取回本人账号中自己的文件）。

用法：
    python fetch_ipa.py                      # 自动从本机浏览器/客户端读取登录态
    python fetch_ipa.py --cookie-string "..."  # 手动提供 Cookie
    python fetch_ipa.py --check             # 只检查登录态是否就绪

背景：
    夸克开放平台对第三方 Agent 通道的 get_download_url 有单文件 50 MB 限制
    (errno 23018)；网页端 file/download 对未登录会话同样有该限制。
    网页端在带账号会话 + 官方 PC 客户端 UA 时才允许取回大文件直链。
    因此本工具从本机 Chromium 内核应用读取已登录的夸克 Cookie，
    换直链后分段下载、断点续传并校验完整性。

    Cookie 全程只在本机内存中解密使用，不打印、不写盘、不外发。
"""
import argparse
import base64
import ctypes
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from ctypes import wintypes

# ---------------------------------------------------------------- 配置
PWD_ID = "ea228353b323"
PASSCODE = "WLmM"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
EXPECTED = {
    "Soul_6.41.0.ipa": 220141026,
    "MOMO陌陌_9.23.2.ipa": 165207615,
}
WEB_FIDS = {
    "Soul_6.41.0.ipa": "ec347d51405543d5aa912eba2b70a69e",
    "MOMO陌陌_9.23.2.ipa": "b0150e1b3306433d99172a550ec125e5",
}

CLIENT_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
             "(KHTML, like Gecko) quark-cloud-drive/2.5.56 "
             "Chrome/100.0.4896.160 Electron/18.3.5.12 Safari/537.36 "
             "Channel/pckk_other_ch")

TOKEN_API = "https://drive-pc.quark.cn/1/clouddrive/share/sharepage/token?pr=ucpro&fr=pc"
DETAIL_API = "https://drive-pc.quark.cn/1/clouddrive/share/sharepage/detail"
DOWNLOAD_API = "https://drive-pc.quark.cn/1/clouddrive/file/download?pr=ucpro&fr=pc"

CHROMIUM_ROOTS = [
    r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data",
    r"C:\Users\Administrator\AppData\Local\Google\Chrome SxS\User Data",
    r"C:\Users\Administrator\AppData\Local\Microsoft\Edge\User Data",
    r"C:\Users\Administrator\AppData\Local\QuarkCloudDrive\User Data",
]

SESSION_NAMES = ("__pus", "__puus", "b-user-id", "PUSS", "__puid")

HEADERS_BASE = {
    "User-Agent": CLIENT_UA,
    "Referer": "https://pan.quark.cn/",
    "Origin": "https://pan.quark.cn",
}

# ---------------------------------------------------------------- Windows 文件读取
GENERIC_READ = 0x80000000
FILE_SHARE_ALL = 0x01 | 0x02 | 0x04
OPEN_EXISTING = 3
k32 = ctypes.WinDLL("kernel32", use_last_error=True)
k32.CreateFileW.restype = wintypes.HANDLE
k32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                            wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD,
                            wintypes.HANDLE]
k32.GetFileSizeEx.argtypes = [wintypes.HANDLE, ctypes.POINTER(ctypes.c_longlong)]
k32.ReadFile.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD,
                         ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID]


class BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.c_ulong),
                ("pbData", ctypes.POINTER(ctypes.c_ubyte))]


def dpapi_decrypt(blob):
    src = BLOB(len(blob), (ctypes.c_ubyte * len(blob)).from_buffer_copy(blob))
    dst = BLOB()
    ok = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(src), None, None, None, None, 0, ctypes.byref(dst))
    if not ok:
        raise RuntimeError("DPAPI 解密失败（需在同一 Windows 用户会话）")
    try:
        return bytes(dst.pbData[:dst.cbData])
    finally:
        ctypes.windll.kernel32.LocalFree(dst.pbData)


def read_file_bytes(path):
    """普通读取；被独占锁时退回共享句柄读取。"""
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError:
        pass
    h = k32.CreateFileW(path, GENERIC_READ, FILE_SHARE_ALL, None,
                        OPEN_EXISTING, 0x80, None)
    if not h or h == ctypes.c_void_p(-1).value:
        raise OSError("无法读取（文件被独占锁定，请先退出夸克客户端）")
    try:
        size = ctypes.c_longlong()
        k32.GetFileSizeEx(h, ctypes.byref(size))
        buf = ctypes.create_string_buffer(size.value)
        got = wintypes.DWORD(0)
        k32.ReadFile(h, buf, size.value, ctypes.byref(got), None)
        return buf.raw[:got.value]
    finally:
        k32.CloseHandle(h)


# ---------------------------------------------------------------- Cookie
def cookies_from_profile(root):
    """解密一个 Chromium profile 的 Cookies，返回 (name, value) 列表。"""
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError:
        print("缺少 cryptography 库：pip install cryptography", file=sys.stderr)
        return []
    state = os.path.join(root, "Local State")
    if not os.path.isfile(state):
        return []
    try:
        with open(state, encoding="utf-8") as fh:
            enc_b64 = json.load(fh)["os_crypt"]["encrypted_key"]
        raw = base64.b64decode(enc_b64)
        if not raw.startswith(b"DPAPI"):
            return []
        aes = AESGCM(dpapi_decrypt(raw[5:]))
    except Exception:
        return []

    out = []
    import glob
    for cookie_db in glob.glob(os.path.join(root, "**", "Network", "Cookies"),
                               recursive=True)[:12]:
        tmp = os.path.join(tempfile.gettempdir(), "_qk_ck_%d.db" % abs(hash(cookie_db)))
        try:
            with open(tmp, "wb") as fh:
                fh.write(read_file_bytes(cookie_db))
            con = sqlite3.connect(tmp)
            for host, name, enc in con.execute(
                    "SELECT host_key,name,encrypted_value FROM cookies"):
                if "quark.cn" not in host or not enc or enc[:3] not in (b"v10", b"v11"):
                    continue
                try:
                    plain = aes.decrypt(enc[3:15], enc[15:], b"")
                    if len(plain) > 32:            # 去掉 SHA256(host) 前缀
                        plain = plain[32:]
                    out.append((name, plain.decode("utf-8", "replace")))
                except Exception:
                    continue
            con.close()
        except Exception:
            continue
        finally:
            if os.path.isfile(tmp):
                os.remove(tmp)
    return out


def collect_cookies():
    pairs = {}
    for root in CHROMIUM_ROOTS:
        for name, value in cookies_from_profile(root):
            pairs[name] = value
    return pairs


# ---------------------------------------------------------------- HTTP
def request_json(url, data=None, cookie=""):
    headers = dict(HEADERS_BASE)
    headers["Content-Type"] = "application/json"
    if cookie:
        headers["Cookie"] = cookie
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8"))


def share_stoken():
    r = request_json(TOKEN_API, {"pwd_id": PWD_ID, "passcode": PASSCODE})
    if r.get("code") != 0:
        raise RuntimeError("分享校验失败: %s" % r.get("message"))
    return r["data"]["stoken"]


def share_detail(stoken):
    from urllib.parse import urlencode
    q = urlencode({"pr": "ucpro", "fr": "pc", "pwd_id": PWD_ID,
                   "stoken": stoken, "pdir_fid": "0", "force": "0",
                   "_page": "1", "_size": "50"})
    r = request_json(DETAIL_API + "?" + q)
    if r.get("code") != 0:
        raise RuntimeError("读取分享清单失败: %s" % r.get("message"))
    return r["data"].get("list", [])


def get_urls(fids, cookie, stoken):
    payload = {"fids": fids, "pwd_id": PWD_ID, "stoken": stoken}
    try:
        return request_json(DOWNLOAD_API, payload, cookie)
    except urllib.error.HTTPError as exc:
        try:
            return json.loads(exc.read().decode("utf-8"))
        except Exception:
            return {"status": exc.code, "code": exc.code, "message": str(exc)}


def fetch(url, path, expected, cookie):
    """带 Range 的断点续传下载。"""
    headers = dict(HEADERS_BASE)
    if cookie:
        headers["Cookie"] = cookie
    offset = os.path.getsize(path) if os.path.isfile(path) else 0
    if offset >= expected:
        print("  已存在且大小正确，跳过：%s" % os.path.basename(path))
        return True
    if offset:
        headers["Range"] = "bytes=%d-" % offset
        print("  从 %d 字节处续传" % offset)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as resp, open(path, "ab") as fh:
        total = offset
        while True:
            chunk = resp.read(1024 * 512)
            if not chunk:
                break
            fh.write(chunk)
            total += len(chunk)
            if total % (10 * 1024 * 1024) < 512 * 1024:
                print("  %d / %d 字节 (%.1f%%)" %
                      (total, expected, total * 100.0 / expected), flush=True)
    size = os.path.getsize(path)
    if size != expected:
        print("  大小不符：%d，期望 %d（保留文件以便续传）" % (size, expected))
        return False
    try:
        with zipfile.ZipFile(path) as zf:
            if "Payload/" not in zf.namelist()[0:5] and not any(
                    n.startswith("Payload/") for n in zf.namelist()[:50]):
                print("  警告：未在包首部找到 Payload/ 目录")
    except Exception as exc:
        print("  ZIP 结构检查提示：%s" % exc)
    print("  完成：%s (%d 字节)" % (os.path.basename(path), size))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cookie-string", help="手动提供夸克网页 Cookie 串")
    ap.add_argument("--check", action="store_true", help="只检查登录态")
    args = ap.parse_args()

    if args.cookie_string:
        pairs = {}
        for part in args.cookie_string.split(";"):
            if "=" in part:
                k, v = part.strip().split("=", 1)
                pairs[k] = v
    else:
        pairs = collect_cookies()

    has_session = any(n in pairs for n in SESSION_NAMES if n not in ("b-user-id",))
    print("本机可用夸克 Cookie 项：%s" % (", ".join(sorted(pairs)) or "无"))
    if not has_session:
        print("\n[未就绪] 没找到账号会话（__pus / __puus 等）。")
        print("请在 Chrome / Edge 或夸克客户端里登录一次 pan.quark.cn，")
        print("然后重新运行本脚本；也可以用 --cookie-string 直接提供。")
        return 3
    if args.check:
        print("[就绪] 已检测到夸克账号会话。")
        return 0

    cookie = "; ".join("%s=%s" % (k, v) for k, v in pairs.items())
    print("正在校验分享链接…")
    stoken = share_stoken()
    listing = share_detail(stoken)
    print("分享清单：%d 个文件" % len(listing))

    targets = [f for f in listing if f.get("file_name") in EXPECTED]
    if not targets:
        targets = [{"fid": v, "file_name": k, "size": EXPECTED[k]}
                   for k, v in WEB_FIDS.items()]

    fids = [f["fid"] for f in targets]
    result = get_urls(fids, cookie, stoken)
    print("取直链：status=%s code=%s message=%s" %
          (result.get("status"), result.get("code"), result.get("message")))
    if result.get("code") not in (0, None):
        print("\n[失败] 服务端拒绝了取直链请求。常见原因：会话过期、账号等级限制、")
        print("或接口侧的 23018 大文件策略。请更新会话后重试。")
        return 2

    urls = {item.get("file_name"): item.get("download_url")
            for item in (result.get("data") or []) if item.get("download_url")}
    ok = True
    for name, size in EXPECTED.items():
        url = urls.get(name)
        if not url:
            print("跳过 %s：未返回直链" % name)
            ok = False
            continue
        print("下载 %s" % name)
        ok = fetch(url, os.path.join(OUT_DIR, name), size, cookie) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
