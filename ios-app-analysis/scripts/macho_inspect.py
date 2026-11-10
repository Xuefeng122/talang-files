#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iOS IPA / Mach-O 结构体检（只读、跨平台、纯标准库）

用途：对本地 IPA 做中性的架构与防护机制盘点，输出 JSON + Markdown 摘要。
范围：只解析文件结构与公开元数据，不修改任何文件，不定位业务方法，
      不提供绕过任何技术措施的指引。

用法：
    python macho_inspect.py <path-to.ipa> [--out <报告目录>]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import plistlib
import re
import struct
import sys
import zipfile
from datetime import datetime, timezone

FAT_MAGIC = 0xCAFEBABE
FAT_MAGIC_64 = 0xCAFEBABF
MH_MAGIC_64 = 0xFEEDFACF
MH_CIGAM_64 = 0xCFFAEDFE
MH_MAGIC = 0xFEEDFACE

CPU_TYPES = {12: "ARM", 0x0100000C: "ARM64", 0x0200000C: "ARM64_32", 7: "x86", 0x01000007: "x86_64"}
FILE_TYPES = {1: "MH_OBJECT", 2: "MH_EXECUTE", 3: "MH_FVMLIB", 4: "MH_CORE",
              5: "MH_PRELOAD", 6: "MH_DYLIB", 7: "MH_DYLINKER", 8: "MH_BUNDLE",
              9: "MH_DYLIB_STUB", 10: "MH_DSYM", 11: "MH_KEXT_BUNDLE"}

LC_NAMES = {
    0x01: "LC_SEGMENT", 0x02: "LC_SYMTAB", 0x0B: "LC_DYSYMTAB",
    0x0C: "LC_LOAD_DYLIB", 0x0D: "LC_ID_DYLIB", 0x0E: "LC_LOAD_DYLINKER",
    0x0F: "LC_ID_DYLINKER", 0x12: "LC_SUB_FRAMEWORK", 0x18: "LC_LOAD_WEAK_DYLIB",
    0x19: "LC_SEGMENT_64", 0x1A: "LC_ROUTINES_64", 0x1B: "LC_UUID",
    0x1C: "LC_RPATH", 0x1D: "LC_CODE_SIGNATURE", 0x1E: "LC_SEGMENT_SPLIT_INFO",
    0x21: "LC_ENCRYPTION_INFO", 0x22: "LC_DYLD_INFO", 0x25: "LC_VERSION_MIN_IPHONEOS",
    0x26: "LC_FUNCTION_STARTS", 0x29: "LC_DATA_IN_CODE", 0x2A: "LC_SOURCE_VERSION",
    0x2B: "LC_DYLIB_CODE_SIGN_DRS", 0x2C: "LC_ENCRYPTION_INFO_64",
    0x2D: "LC_LINKER_OPTION", 0x2E: "LC_LINKER_OPTIMIZATION_HINT",
    0x32: "LC_BUILD_VERSION", 0x33: "LC_DYLD_EXPORTS_TRIE", 0x34: "LC_DYLD_CHAINED_FIXUPS",
    0x8000001C: "LC_RPATH", 0x80000018: "LC_LOAD_WEAK_DYLIB",
    0x8000001F: "LC_REEXPORT_DYLIB", 0x80000023: "LC_LOAD_UPWARD_DYLIB",
}

MH_FLAGS = {
    0x1: "MH_NOUNDEFS", 0x2: "MH_INCRLINK", 0x4: "MH_DYLDLINK",
    0x8: "MH_BINDATLOAD", 0x10: "MH_PREBOUND", 0x20: "MH_SPLIT_SEGS",
    0x80: "MH_TWOLEVEL", 0x100: "MH_FORCE_FLAT", 0x200: "MH_NOMULTIDEFS",
    0x400: "MH_NOFIXPREBINDING", 0x800: "MH_PREBINDABLE", 0x1000: "MH_ALLMODSBOUND",
    0x2000: "MH_SUBSECTIONS_VIA_SYMBOLS", 0x4000: "MH_CANONICAL",
    0x8000: "MH_WEAK_DEFINES", 0x10000: "MH_BINDS_TO_WEAK",
    0x20000: "MH_ALLOW_STACK_EXECUTION", 0x40000: "MH_ROOT_SAFE",
    0x80000: "MH_SETUID_SAFE", 0x100000: "MH_NO_REEXPORTED_DYLIBS",
    0x200000: "MH_PIE", 0x400000: "MH_DEAD_STRIPPABLE_DYLIB",
    0x800000: "MH_HAS_TLV_DESCRIPTORS", 0x1000000: "MH_NO_HEAP_EXECUTION",
    0x02000000: "MH_APP_EXTENSION_SAFE",
}

# 只用于观察"是否存在防护/运行时检测字符串"，不做任何绕过推断。
GUARD_TOKENS = [
    "DYLD_INSERT_LIBRARIES", "MobileSubstrate", "Substrate", "libhooker", "Frida",
    "frida", "gum-js-loop", "cycript", "ptrace", "sysctl", "amfid",
    "jailbreak", "Jailbreak", "jailbroken", "/Applications/Cydia.app",
    "cydia", "apticket", "fork()", "posix_spawn", "task_for_pid",
    "SSLKillSwitch", "SSLSetSessionOption", "SecTrustEvaluate",
    "NSURLSession", "ATS", "CFNetwork", "os_proc", "objc_msgSend",
]


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def cstr(blob: bytes, offset: int, limit: int) -> str:
    if offset < 0 or offset >= limit:
        return ""
    end = blob.find(b"\x00", offset, limit)
    if end < 0:
        end = limit
    return blob[offset:end].decode("utf-8", "replace")


def parse_slice(data: bytes, base: int, size: int, arch_label: str) -> dict:
    blob = data[base:base + size]
    info = {"arch_label": arch_label, "slice_offset": base, "slice_size": size}
    if len(blob) < 32:
        info["error"] = "slice too short"
        return info

    magic = struct.unpack_from("<I", blob, 0)[0]
    if magic == MH_MAGIC_64:
        endian = "<"
    elif magic == MH_CIGAM_64 or magic == MH_MAGIC:
        endian = ">"
    else:
        info["error"] = f"unsupported magic 0x{magic:08x}"
        return info

    (_, cputype, cpusubtype, filetype, ncmds, sizeofcmds, flags, _) = struct.unpack_from(
        endian + "IiiIIIII", blob, 0)
    info.update({
        "magic": f"0x{magic:08x}",
        "cpu_type": CPU_TYPES.get(cputype, f"0x{cputype:08x}"),
        "cpu_subtype": f"0x{cpusubtype:08x}",
        "filetype": FILE_TYPES.get(filetype, str(filetype)),
        "ncmds": ncmds,
        "sizeofcmds": sizeofcmds,
        "flags": [name for bit, name in MH_FLAGS.items() if flags & bit],
        "load_commands": [],
        "segments": [],
        "sections": [],
        "dylibs": [],
        "rpaths": [],
        "encryption": None,
        "uuid": None,
        "build_version": None,
        "code_signature": None,
    })

    pos = 32
    cmd_end = min(pos + sizeofcmds, len(blob))
    for _ in range(ncmds):
        if pos + 8 > cmd_end:
            break
        cmd, cmdsize = struct.unpack_from(endian + "II", blob, pos)
        name = LC_NAMES.get(cmd, f"LC_0x{cmd:08X}")
        info["load_commands"].append(name)
        limit = min(pos + cmdsize, len(blob))

        if cmd == 0x19:  # LC_SEGMENT_64
            segname = cstr(blob, pos + 8, pos + 24)
            vmaddr, vmsize, fileoff, filesize = struct.unpack_from(endian + "QQQQ", blob, pos + 24)
            maxprot, initprot, nsects, _ = struct.unpack_from(endian + "iiII", blob, pos + 56)
            info["segments"].append({
                "name": segname, "vmaddr": hex(vmaddr), "vmsize": vmsize,
                "fileoff": fileoff, "filesize": filesize,
                "initprot": initprot, "maxprot": maxprot, "nsects": nsects,
            })
            sect = pos + 72
            for _ in range(nsects):
                if sect + 80 > limit:
                    break
                sname = cstr(blob, sect, sect + 16)
                sseg = cstr(blob, sect + 16, sect + 32)
                addr, ssize = struct.unpack_from(endian + "QQ", blob, sect + 32)
                info["sections"].append({"name": sname, "segment": sseg, "size": ssize, "addr": hex(addr)})
                sect += 80

        elif cmd in (0x0C, 0x18, 0x0D, 0x8000001C, 0x80000018, 0x8000001F, 0x80000023):
            name_off = struct.unpack_from(endian + "I", blob, pos + 8)[0]
            value = cstr(blob, pos + name_off, limit)
            if cmd in (0x1C, 0x8000001C):
                info["rpaths"].append(value)
            else:
                info["dylibs"].append({"load_command": name, "name": value})

        elif cmd == 0x1B and limit >= pos + 24:
            info["uuid"] = blob[pos + 8:pos + 24].hex().upper()

        elif cmd in (0x21, 0x2C) and limit >= pos + 24:
            cryptoff, cryptsize, cryptid = struct.unpack_from(endian + "III", blob, pos + 8)
            info["encryption"] = {"cryptoff": cryptoff, "cryptsize": cryptsize,
                                  "cryptid": cryptid,
                                  "state": "encrypted (App Store DRM)" if cryptid else "not encrypted"}

        elif cmd == 0x1D and limit >= pos + 16:
            dataoff, datasize = struct.unpack_from(endian + "II", blob, pos + 8)
            info["code_signature"] = {"dataoff": dataoff, "datasize": datasize}

        elif cmd == 0x32 and limit >= pos + 24:
            platform, minos, sdk, ntools = struct.unpack_from(endian + "IIII", blob, pos + 8)
            def ver(v):
                return f"{(v >> 16) & 0xFFFF}.{(v >> 8) & 0xFF}.{v & 0xFF}"
            info["build_version"] = {"platform": platform, "minos": ver(minos), "sdk": ver(sdk), "ntools": ntools}

        elif cmd == 0x25 and limit >= pos + 16:
            v, sdk = struct.unpack_from(endian + "II", blob, pos + 8)
            def ver2(x):
                return f"{(x >> 16) & 0xFFFF}.{(x >> 8) & 0xFF}.{x & 0xFF}"
            info["build_version"] = {"minos": ver2(v), "sdk": ver2(sdk), "via": "LC_VERSION_MIN_IPHONEOS"}

        if cmdsize < 8:
            break
        pos += cmdsize

    # 防护特征观察：仅统计可打印字符串中出现的公开检测关键字。
    hits = {}
    for token in GUARD_TOKENS:
        count = blob.count(token.encode("ascii", "ignore"))
        if count:
            hits[token] = count
    info["guard_token_hits"] = hits
    return info


def parse_macho(data: bytes) -> dict:
    result = {"slices": []}
    if len(data) < 8:
        result["error"] = "file too short"
        return result
    magic_be = struct.unpack_from(">I", data, 0)[0]
    if magic_be in (FAT_MAGIC, FAT_MAGIC_64):
        nfat = struct.unpack_from(">I", data, 4)[0]
        entry_size = 32 if magic_be == FAT_MAGIC_64 else 20
        result["container"] = "FAT64" if magic_be == FAT_MAGIC_64 else "FAT"
        for i in range(min(nfat, 16)):
            off = 8 + i * entry_size
            if off + entry_size > len(data):
                break
            cputype, cpusubtype, soff, ssize, align = struct.unpack_from(">iiIII", data, off)
            label = f"{CPU_TYPES.get(cputype, hex(cputype))}/0x{cpusubtype:08x}"
            result["slices"].append(parse_slice(data, soff, ssize, label))
    else:
        result["container"] = "thin"
        result["slices"].append(parse_slice(data, 0, len(data), "single"))
    return result


def find_app_dir(root: str):
    for dirpath, dirnames, _ in os.walk(root):
        for d in dirnames:
            if d.endswith(".app"):
                return os.path.join(dirpath, d)
    return None


def inspect(ipa_path: str) -> dict:
    report = {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "input": os.path.abspath(ipa_path),
        "size": os.path.getsize(ipa_path),
        "sha256": sha256_of(ipa_path),
        "app": {},
        "macho": {},
        "bundle_files": {},
        "notes": [],
    }
    if zipfile.is_zipfile(ipa_path):
        with zipfile.ZipFile(ipa_path) as zf:
            names = zf.namelist()
            exts = {}
            for n in names:
                ext = os.path.splitext(n)[1].lower() or "(no ext)"
                exts[ext] = exts.get(ext, 0) + 1
            report["bundle_files"] = {
                "entry_count": len(names),
                "extension_histogram": dict(sorted(exts.items(), key=lambda kv: -kv[1])[:20]),
                "frameworks": sorted({m.group(1) for n in names
                                      for m in [re.search(r"([^/]+\.framework)/", n)] if m}),
                "dynamic_libraries": [n for n in names if n.lower().endswith((".dylib", ".framework/"))],
                "has_mobileprovision": any(n.endswith("embedded.mobileprovision") for n in names),
                "has_code_signature_dir": any("_CodeSignature/" in n for n in names),
                "has_privacy_manifest": any(n.endswith("PrivacyInfo.xcprivacy") for n in names),
            }
            # 只把 .app 下的 Info.plist 与主可执行文件读进内存，不落盘。
            info_name = next((n for n in names if n.endswith(".app/Info.plist")), None)
            exe_name = None
            if info_name:
                try:
                    info = plistlib.loads(zf.read(info_name))
                except Exception as exc:
                    info = {}
                    report["notes"].append(f"Info.plist parse failed: {exc}")
                keys = ["CFBundleIdentifier", "CFBundleExecutable", "CFBundleShortVersionString",
                        "CFBundleVersion", "MinimumOSVersion", "CFBundleSupportedPlatforms",
                        "UIDeviceFamily", "NSAppTransportSecurity", "CFBundleURLTypes",
                        "UISupportedInterfaceOrientations", "ITSAppUsesNonExemptEncryption",
                        "NSCameraUsageDescription", "NSPhotoLibraryUsageDescription",
                        "NSMicrophoneUsageDescription", "NSLocationWhenInUseUsageDescription"]
                report["app"] = {k: info.get(k) for k in keys if k in info}
                exe = info.get("CFBundleExecutable")
                if exe:
                    prefix = info_name[:-len("Info.plist")]
                    exe_name = prefix + exe
            if exe_name and exe_name in names:
                data = zf.read(exe_name)
                report["app"]["executable"] = exe_name
                report["app"]["executable_size"] = len(data)
                report["macho"] = parse_macho(data)
            else:
                report["notes"].append("main executable not found in archive")
    else:
        with open(ipa_path, "rb") as fh:
            report["macho"] = parse_macho(fh.read())
        report["notes"].append("input treated as raw Mach-O")
    return report


def to_markdown(r: dict) -> str:
    lines = ["# iOS 应用结构体检报告", "",
             f"- 生成时间：{r['generated_at']}",
             f"- 输入文件：`{r['input']}`",
             f"- 文件大小：{r['size'] / 1024 / 1024:.2f} MiB",
             f"- SHA-256：`{r['sha256']}`", ""]

    if r.get("app"):
        lines += ["## 应用元数据", "", "| 字段 | 值 |", "| --- | --- |"]
        for k, v in r["app"].items():
            text = str(v).replace("|", "\\|").replace("\n", " ")
            if len(text) > 160:
                text = text[:160] + " ..."
            lines.append(f"| `{k}` | {text} |")
        lines.append("")

    bf = r.get("bundle_files") or {}
    if bf:
        lines += ["## 包内容概览", "",
                  f"- 条目总数：{bf.get('entry_count', 0)}",
                  f"- 内嵌 framework：{len(bf.get('frameworks', []))} 个",
                  f"- 动态库/framework 路径：{len(bf.get('dynamic_libraries', []))} 条",
                  f"- 含描述文件：{'是' if bf.get('has_mobileprovision') else '否'}",
                  f"- 含代码签名目录：{'是' if bf.get('has_code_signature_dir') else '否'}",
                  f"- 含隐私清单 PrivacyInfo.xcprivacy：{'是' if bf.get('has_privacy_manifest') else '否'}",
                  ""]
        if bf.get("frameworks"):
            lines += ["### 内嵌 framework（前 30）", ""]
            lines += [f"- `{n}`" for n in bf["frameworks"][:30]]
            lines.append("")
        if bf.get("extension_histogram"):
            lines += ["### 文件类型分布（前 12）", "", "| 扩展名 | 数量 |", "| --- | ---: |"]
            for ext, count in list(bf["extension_histogram"].items())[:12]:
                lines.append(f"| `{ext}` | {count} |")
            lines.append("")

    macho = r.get("macho") or {}
    lines += [f"## Mach-O 结构（容器：{macho.get('container', 'n/a')}）", ""]
    for s in macho.get("slices", []):
        if s.get("error"):
            lines += [f"### 切片 {s['arch_label']} — 解析失败：{s['error']}", ""]
            continue
        lines += [f"### 切片 {s['arch_label']}", "",
                  f"- 类型：{s['filetype']} / CPU：{s['cpu_type']} / 子类型：{s['cpu_subtype']}",
                  f"- 加载命令：{s['ncmds']} 条，共 {s['sizeofcmds']} 字节",
                  f"- 编译标志：{', '.join(s['flags']) or '（无常见标志）'}",
                  f"- UUID：{s.get('uuid') or '未声明'}",
                  f"- 构建版本：{s.get('build_version') or '未声明'}",
                  f"- 加密状态：{s['encryption']['state'] if s.get('encryption') else '未声明 LC_ENCRYPTION_INFO'}",
                  f"- 代码签名：{'有' if s.get('code_signature') else '无'}",
                  f"- 依赖 dylib：{len(s['dylibs'])} 个 / rpath：{len(s['rpaths'])} 条", ""]
        if s.get("segments"):
            lines += ["| 段 | VM 大小 | 文件偏移 | 节数 |", "| --- | ---: | ---: | ---: |"]
            for seg in s["segments"]:
                lines.append(f"| `{seg['name']}` | {seg['vmsize']} | {seg['fileoff']} | {seg['nsects']} |")
            lines.append("")
        if s.get("dylibs"):
            lines += ["<details><summary>依赖库清单</summary>", ""]
            lines += [f"- `{d['name']}` （{d['load_command']}）" for d in s["dylibs"]]
            lines += ["", "</details>", ""]
        hits = s.get("guard_token_hits") or {}
        if hits:
            lines += ["**防护/运行时检测字符串观察**（仅统计字面量出现次数，不做绕过推断）", "",
                      "| 关键字 | 出现次数 |", "| --- | ---: |"]
            for k, v in sorted(hits.items(), key=lambda kv: -kv[1]):
                lines.append(f"| `{k}` | {v} |")
            lines.append("")

    if r.get("notes"):
        lines += ["## 备注", ""] + [f"- {n}" for n in r["notes"]] + [""]
    lines += ["---", "",
              "本报告只记录文件结构与公开元数据，用于学习 iOS 二进制组织方式与安全加固现状；",
              "不包含、也不构成对任何技术措施的规避方法。", ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="只读的 iOS IPA / Mach-O 结构体检工具")
    ap.add_argument("ipa", help="IPA 或 Mach-O 文件路径")
    ap.add_argument("--out", help="报告输出目录", default=None)
    args = ap.parse_args()

    if not os.path.isfile(args.ipa):
        print(f"[!] 文件不存在: {args.ipa}", file=sys.stderr)
        return 2

    report = inspect(args.ipa)
    out_dir = args.out or os.path.join(os.path.dirname(os.path.abspath(args.ipa)), "report")
    os.makedirs(out_dir, exist_ok=True)
    stem = re.sub(r"[^A-Za-z0-9_.-]", "_", os.path.splitext(os.path.basename(args.ipa))[0])
    json_path = os.path.join(out_dir, f"{stem}.structure.json")
    md_path = os.path.join(out_dir, f"{stem}.structure.md")
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(to_markdown(report))
    print(f"[+] JSON : {json_path}")
    print(f"[+] MD   : {md_path}")
    enc = [s.get("encryption") for s in report.get("macho", {}).get("slices", []) if s.get("encryption")]
    print(f"[+] 切片数: {len(report.get('macho', {}).get('slices', []))}  加密标记: {enc or '无'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
