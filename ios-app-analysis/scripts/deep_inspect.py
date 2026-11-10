#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iOS Mach-O 深度静态结构解析（只读、跨平台、纯标准库）

与 macho_inspect.py 的分工：
  - macho_inspect.py : 包/容器层体检（IPA 清单、加载命令、段表概览）
  - deep_inspect.py  : 二进制内部层（符号表、ObjC 元数据节、代码签名、
                       导出 trie、字符串常量、依赖库归类、技术栈推断）

严格边界：
  * 只解析文件内已存在的静态结构与公开元数据，不执行、不修改任何文件；
  * 只输出统计与结构性归类，不逐条输出业务类名/方法名，
    不定位任何业务方法，不提供规避技术措施的指引；
  * 不生成反编译伪代码（那需要函数级反编译器后端）。

用法：
    python deep_inspect.py <path-to.ipa|Mach-O> [--out <报告目录>]
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
from collections import Counter
from datetime import datetime, timezone

LC_REQ_DYLD = 0x80000000

MH_MAGIC_64 = 0xFEEDFACF
MH_CIGAM_64 = 0xCFFAEDFE
MH_MAGIC = 0xFEEDFACE
FAT_MAGIC = 0xCAFEBABE
FAT_MAGIC_64 = 0xCAFEBABF

CPU_TYPES = {12: "ARM", 0x0100000C: "ARM64", 0x0200000C: "ARM64_32",
            7: "x86", 0x01000007: "x86_64"}
FILE_TYPES = {1: "MH_OBJECT", 2: "MH_EXECUTE", 3: "MH_FVMLIB", 4: "MH_CORE",
              5: "MH_PRELOAD", 6: "MH_DYLIB", 7: "MH_DYLINKER", 8: "MH_BUNDLE",
              9: "MH_DYLIB_STUB", 10: "MH_DSYM", 11: "MH_KEXT_BUNDLE"}
PLATFORMS = {1: "macOS", 2: "iOS", 3: "tvOS", 4: "watchOS",
             5: "bridgeOS", 6: "macCatalyst", 7: "iOSSimulator",
             8: "tvOSSimulator", 9: "watchOSSimulator", 10: "driverKit",
             11: "xrOS", 12: "xrOSSimulator"}

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
    0x35: "LC_FILESET_ENTRY", 0x8000001F: "LC_REEXPORT_DYLIB",
    0x80000023: "LC_LOAD_UPWARD_DYLIB", 0x80000027: "LC_VERSION_MIN_MACOSX",
    0x80000018: "LC_LOAD_WEAK_DYLIB", 0x8000001C: "LC_RPATH",
}

MH_FLAGS = {
    0x1: "MH_NOUNDEFS", 0x2: "MH_INCRLINK", 0x4: "MH_DYLD_LINK",
    0x8: "MH_BIND_AT_LOAD", 0x10: "MH_PREBOUND", 0x20: "MH_SPLIT_SEGS",
    0x80: "MH_TWOLEVEL", 0x200: "MH_NOMULTIDEFS", 0x1000: "MH_ALLMODSBOUND",
    0x2000: "MH_SUBSECTIONS_VIA_SYMBOLS", 0x8000: "MH_WEAK_DEFINES",
    0x10000: "MH_BINDS_TO_WEAK", 0x20000: "MH_ALLOW_STACK_EXECUTION",
    0x200000: "MH_PIE", 0x1000000: "MH_NO_HEAP_EXECUTION",
    0x02000000: "MH_APP_EXTENSION_SAFE",
}

# 只做"存在哪些公开技术机制"的中性观察，不做任何绕过推断。
MECHANISM_SYMBOLS = {
    "stack_protector": ["___stack_chk_fail", "___stack_chk_guard"],
    "arc_objc": ["_objc_retain", "_objc_release", "_objc_autoreleasePoolPush"],
    "objc_runtime": ["_objc_msgSend", "_objc_getClass", "_objc_allocateClassPair"],
    "ptrace_debug": ["_ptrace", "_sysctl", "_task_for_pid"],
    "trust_eval": ["_SecTrustEvaluate", "_SecTrustEvaluateWithError",
                    "_SSLSetSessionOption", "_SSLCreateContext"],
    "dyld_introspection": ["_dyld_get_image_name", "_dlopen", "_dlsym",
                            "_DYLD_INSERT_LIBRARIES"],
    "crypto_common": ["_CCCrypt", "_CC_MD5", "_CC_SHA1", "_SecKeyCreateSignature"],
    "keychain": ["_SecItemAdd", "_SecItemCopyMatching"],
}

OBJC_SECTIONS = {
    "__objc_imageinfo", "__objc_classname", "__objc_methname", "__objc_selrefs",
    "__objc_classrefs", "__objc_superrefs", "__objc_classlist", "__objc_catlist",
    "__objc_catsel", "__objc_protolist", "__objc_protorefs", "__objc_const",
    "__objc_data", "__objc_ivar", "__objc_superrefs",
}
SWIFT_SECTIONS = {
    "__swift5_typeref", "__swift5_reflstr", "__swift5_fieldmd", "__swift5_types",
    "__swift5_assocty", "__swift5_proto", "__swift5_protos", "__swift5_capture",
    "__swift5_mpenum", "__swift5_builtin", "__swift3_typeref", "__swift4_typeref",
}


def u32(b, o, e="<"):
    return struct.unpack_from(e + "I", b, o)[0]


def cstr(blob, offset, limit=None):
    if offset < 0 or offset >= len(blob):
        return ""
    end = blob.find(b"\x00", offset, limit if limit is not None else len(blob))
    if end < 0:
        end = limit if limit is not None else len(blob)
    return blob[offset:end].decode("utf-8", "replace")


def uleb(buf, pos, limit):
    result = 0
    shift = 0
    while pos < limit and shift < 64:
        byte = buf[pos]
        pos += 1
        result |= (byte & 0x7F) << shift
        if not (byte & 0x80):
            return result, pos
        shift += 7
    return None, pos


def version_str(v):
    return f"{(v >> 16) & 0xFFFF}.{(v >> 8) & 0xFF}.{v & 0xFF}"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# 切片解析
# ---------------------------------------------------------------------------

def parse_slice(blob, base, size, arch_label):
    d = blob[base:base + size]
    out = {
        "arch_label": arch_label,
        "slice_offset": base,
        "slice_size": len(d),
        "load_commands": [],
        "segments": [],
        "sections": [],
        "dylibs": [],
        "rpaths": [],
        "linkedit": {},
        "symbols": {},
        "objc": {},
        "swift": {},
        "strings": {},
        "signature": {},
        "exports": {},
        "mechanisms": {},
        "notes": [],
    }
    if len(d) < 32:
        out["notes"].append("slice too short")
        return out

    magic = u32(d, 0, "<")
    if magic == MH_MAGIC_64:
        e = "<"
    elif magic in (MH_CIGAM_64, MH_MAGIC):
        e = ">"
    else:
        out["notes"].append(f"unsupported magic 0x{magic:08x}")
        return out

    (_, cputype, cpusubtype, filetype, ncmds, sizeofcmds, flags, _) = struct.unpack_from(
        e + "IiiIIIII", d, 0)
    out.update({
        "magic": f"0x{magic:08x}",
        "cpu_type": CPU_TYPES.get(cputype, hex(cputype)),
        "cpu_subtype": hex(cpusubtype),
        "filetype": FILE_TYPES.get(filetype, str(filetype)),
        "ncmds": ncmds,
        "sizeofcmds": sizeofcmds,
        "flags": [n for bit, n in MH_FLAGS.items() if flags & bit],
        "pie": bool(flags & 0x200000),
    })

    pos = 32
    cmd_end = min(pos + sizeofcmds, len(d))
    symtab = None
    for _ in range(ncmds):
        if pos + 8 > cmd_end:
            break
        cmd, cmdsize = struct.unpack_from(e + "II", d, pos)
        base_cmd = cmd & ~LC_REQ_DYLD
        name = LC_NAMES.get(cmd, LC_NAMES.get(base_cmd, f"LC_0x{cmd:08X}"))
        out["load_commands"].append({"name": name, "cmd": hex(cmd), "size": cmdsize})
        limit = min(pos + cmdsize, len(d))
        if cmdsize < 8:
            break

        if base_cmd == 0x19:  # LC_SEGMENT_64
            segname = cstr(d, pos + 8, pos + 24)
            vmaddr, vmsize, fileoff, filesize = struct.unpack_from(e + "QQQQ", d, pos + 24)
            maxprot, initprot, nsects, segflags = struct.unpack_from(e + "iiII", d, pos + 56)
            out["segments"].append({
                "name": segname, "vmaddr": hex(vmaddr), "vmsize": vmsize,
                "fileoff": fileoff, "filesize": filesize,
                "initprot": initprot, "maxprot": maxprot, "nsects": nsects,
            })
            sect = pos + 72
            for _ in range(nsects):
                if sect + 80 > limit:
                    break
                sname = cstr(d, sect, sect + 16)
                sseg = cstr(d, sect + 16, sect + 32)
                addr, ssize = struct.unpack_from(e + "QQ", d, sect + 32)
                (soff, align, reloff, nreloc, sflags,
                 r1, r2, r3) = struct.unpack_from(e + "IIIIIIII", d, sect + 48)
                out["sections"].append({
                    "name": sname, "segment": sseg, "addr": hex(addr), "size": ssize,
                    "offset": soff, "align": align, "flags": hex(sflags),
                    "reserved1": r1, "reserved2": r2,
                })
                sect += 80

        elif base_cmd in (0x0C, 0x0D, 0x18, 0x1F, 0x23, 0x1C):
            noff = u32(d, pos + 8, e)
            value = cstr(d, pos + noff, limit)
            if base_cmd == 0x1C:
                out["rpaths"].append(value)
            else:
                out["dylibs"].append({"command": name, "name": value})

        elif base_cmd == 0x1B and limit >= pos + 24:
            out["uuid"] = d[pos + 8:pos + 24].hex().upper()

        elif base_cmd in (0x21, 0x2C) and limit >= pos + 24:
            cryptoff, cryptsize, cryptid = struct.unpack_from(e + "III", d, pos + 8)
            out["encryption"] = {
                "cryptoff": cryptoff, "cryptsize": cryptsize, "cryptid": cryptid,
                "state": "encrypted" if cryptid else "not encrypted (decrypted image)",
            }

        elif base_cmd == 0x1D and limit >= pos + 16:
            dataoff, datasize = struct.unpack_from(e + "II", d, pos + 8)
            out["linkedit"]["code_signature"] = {"offset": dataoff, "size": datasize}

        elif base_cmd in (0x26, 0x29, 0x33, 0x34, 0x1E, 0x22) and limit >= pos + 16:
            dataoff, datasize = struct.unpack_from(e + "II", d, pos + 8)
            key = {
                0x26: "function_starts", 0x29: "data_in_code", 0x33: "exports_trie",
                0x34: "chained_fixups", 0x1E: "segment_split_info", 0x22: "dyld_info",
            }[base_cmd]
            out["linkedit"][key] = {"offset": dataoff, "size": datasize}

        elif base_cmd == 0x2 and limit >= pos + 24:
            symoff, nsyms, stroff, strsize = struct.unpack_from(e + "IIII", d, pos + 8)
            symtab = (symoff, nsyms, stroff, strsize)

        elif base_cmd == 0x0B and limit >= pos + 80:
            vals = struct.unpack_from(e + "IIIIIIIIIIIIIIIIII", d, pos + 8)
            keys = ["ilocalsym", "nlocalsym", "iextdefsym", "nextdefsym",
                    "iundefsym", "nundefsym", "tocoff", "ntoc", "modtaboff",
                    "nmodtab", "extrefsymoff", "nextrefsyms", "indirectsymoff",
                    "nindirectsyms", "extreloff", "nextrel", "locreloff", "nlocrel"]
            out["dysymtab"] = dict(zip(keys, vals))

        elif base_cmd == 0x32 and limit >= pos + 24:
            platform, minos, sdk, ntools = struct.unpack_from(e + "IIII", d, pos + 8)
            out["build_version"] = {
                "platform": PLATFORMS.get(platform, str(platform)),
                "minos": version_str(minos), "sdk": version_str(sdk), "ntools": ntools,
            }

        elif base_cmd == 0x25 and limit >= pos + 16:
            v, sdk = struct.unpack_from(e + "II", d, pos + 8)
            out["build_version"] = {"minos": version_str(v), "sdk": version_str(sdk),
                                    "via": "LC_VERSION_MIN_IPHONEOS"}

        elif base_cmd == 0x2A and limit >= pos + 16:
            out["source_version"] = struct.unpack_from(e + "Q", d, pos + 8)[0]

        pos += cmdsize

    # ---- 符号表 ----
    if symtab:
        symoff, nsyms, stroff, strsize = symtab
        out["symbols"] = parse_symbols(d, symoff, nsyms, stroff, strsize, e)

    # ---- 节数据（ObjC / Swift / 字符串）----
    section_index = {(s["segment"], s["name"]): s for s in out["sections"]}
    out["objc"] = parse_objc_sections(d, base, section_index)
    out["swift"] = parse_swift_sections(section_index)
    out["strings"] = parse_string_sections(d, base, section_index)

    # ---- 技术机制观察（基于符号名与节名）----
    symnames = out["symbols"].get("name_set", set())
    mech = {}
    for group, needles in MECHANISM_SYMBOLS.items():
        found = sorted({n for n in needles if n in symnames})
        if found:
            mech[group] = found
    out["mechanisms"] = mech
    out["symbols"].pop("name_set", None)

    # ---- 代码签名 ----
    if "code_signature" in out["linkedit"]:
        out["signature"] = parse_code_signature(d, base,
                                                 out["linkedit"]["code_signature"])

    # ---- 导出 trie ----
    if "exports_trie" in out["linkedit"]:
        out["exports"] = parse_export_trie(d, base, out["linkedit"]["exports_trie"])

    # ---- 依赖库归类 ----
    out["dylib_groups"] = classify_dylibs(out["dylibs"])
    # ---- 技术栈推断 ----
    out["stack_inference"] = infer_stack(out)
    return out


def parse_symbols(d, symoff, nsyms, stroff, strsize, e):
    res = {"count": nsyms, "string_table_size": strsize, "type_counts": {},
           "class_count": 0, "category_counts": {}, "prefix_histogram": {},
           "sample_structural_symbols": []}
    if symoff <= 0 or nsyms <= 0 or symoff + nsyms * 16 > len(d):
        res["note"] = "symbol table out of range or absent (stripped)"
        return res
    strtab = d[stroff:stroff + min(strsize, len(d) - stroff)]
    names = set()
    type_counts = Counter()
    cat = Counter()
    prefixes = Counter()
    samples = []
    fmt = e + "IBBHQ"
    for i in range(nsyms):
        try:
            n_strx, n_type, n_sect, n_desc, n_value = struct.unpack_from(fmt, d, symoff + i * 16)
        except struct.error:
            break
        ntype = n_type & 0x0E
        type_names = {0x00: "N_UNDF (undefined/import)", 0x02: "N_ABS", 0x0A: "N_INDR",
                      0x0C: "N_PBUD", 0x0E: "N_SECT (defined)"}
        type_counts[type_names.get(ntype, hex(ntype))] += 1
        if n_strx <= 0 or n_strx >= len(strtab):
            continue
        name = cstr(strtab, n_strx)
        if not name:
            continue
        names.add(name)
        if name.startswith("_OBJC_CLASS_$_"):
            cat["objc_class"] += 1
            cls = name[len("_OBJC_CLASS_$_"):]
            prefixes[class_prefix(cls)] += 1
        elif name.startswith("_OBJC_METACLASS_$_"):
            cat["objc_metaclass"] += 1
        elif name.startswith("_OBJC_IVAR_$_"):
            cat["objc_ivar"] += 1
        elif name.startswith("_OBJC_PROTOCOL_$_"):
            cat["objc_protocol"] += 1
        elif name.startswith("_$s") or name.startswith("_$S") or name.startswith("__swift"):
            cat["swift_mangled"] += 1
        elif name.startswith("__Z") or name.startswith("__ZN"):
            cat["cpp_mangled"] += 1
        elif name.startswith("_objc_") or name.startswith("_OSAtomic"):
            cat["objc_runtime"] += 1
        else:
            cat["other"] += 1
        if len(samples) < 12 and (name.startswith("_objc_") or name.startswith("__swift")):
            samples.append(name)
    res.update({
        "type_counts": dict(type_counts),
        "category_counts": dict(cat),
        "class_count": cat.get("objc_class", 0),
        "prefix_histogram": dict(prefixes.most_common(24)),
        "sample_structural_symbols": samples,
    })
    res["name_set"] = names
    return res


def class_prefix(cls):
    """按驼峰边界取一个保守的模块前缀，仅用于统计聚类，不输出业务类名。"""
    if cls.startswith(("NS", "UI", "CA", "CG", "CF", "WK", "AV", "CL", "MK", "PH")):
        return cls[:2]
    m = re.match(r"^([A-Z]{2,6})(?=[A-Z][a-z]|_|$|\d)", cls)
    if m:
        return m.group(1)
    m = re.match(r"^([A-Z][a-z]{2,7})", cls)
    return m.group(1) if m else (cls[:4] if cls else "(other)")


def section_bytes(d, base, s):
    off = s["offset"] - base if s["offset"] >= base else s["offset"]
    size = min(s["size"], max(0, len(d) - off))
    if off < 0 or size <= 0:
        return b""
    return d[off:off + size]


def parse_objc_sections(d, base, index):
    out = {"present_sections": {}, "classname_count": 0, "methname_count": 0,
           "selector_refs": 0, "class_refs": 0, "super_refs": 0,
           "classlist_entries": 0, "category_entries": 0, "protocol_entries": 0}
    for (seg, name), s in index.items():
        if name not in OBJC_SECTIONS:
            continue
        out["present_sections"][f"{seg},{name}"] = {"size": s["size"],
                                                   "addr": s["addr"]}
        raw = section_bytes(d, base, s)
        if name == "__objc_classname":
            out["classname_count"] = count_cstrings(raw)
        elif name == "__objc_methname":
            out["methname_count"] = count_cstrings(raw)
        elif name == "__objc_selrefs":
            out["selector_refs"] = s["size"] // 8
        elif name == "__objc_classrefs":
            out["class_refs"] = s["size"] // 8
        elif name == "__objc_superrefs":
            out["super_refs"] = s["size"] // 8
        elif name == "__objc_classlist":
            out["classlist_entries"] = s["size"] // 8
        elif name == "__objc_catlist":
            out["category_entries"] = s["size"] // 8
        elif name == "__objc_protolist":
            out["protocol_entries"] = s["size"] // 8
    return out


def parse_swift_sections(index):
    present = [f"{seg},{name}" for (seg, name), s in index.items()
               if name in SWIFT_SECTIONS]
    return {"present_sections": sorted(present), "section_count": len(present)}


def count_cstrings(raw):
    if not raw:
        return 0
    return sum(1 for part in raw.split(b"\x00") if part)


def parse_string_sections(d, base, index):
    out = {"sections": {}}
    for (seg, name), s in index.items():
        if name in ("__cstring", "__ustring", "__cfstring", "__const"):
            raw = section_bytes(d, base, s)
            if not raw:
                continue
            if name == "__cstring":
                parts = [p for p in raw.split(b"\x00") if p]
                lens = [len(p) for p in parts]
                out["sections"][f"{seg},{name}"] = {
                    "size": s["size"], "string_count": len(parts),
                    "max_len": max(lens) if lens else 0,
                    "avg_len": round(sum(lens) / len(lens), 1) if lens else 0,
                }
            else:
                out["sections"][f"{seg},{name}"] = {"size": s["size"]}
    return out


def parse_code_signature(d, base, info):
    off = info["offset"] - base if info["offset"] >= base else info["offset"]
    size = min(info["size"], max(0, len(d) - off))
    out = {"offset": info["offset"], "size": info["size"], "blobs": [], "notes": []}
    if off < 0 or size < 8:
        out["notes"].append("signature blob out of range")
        return out
    blob = d[off:off + size]
    magic = struct.unpack_from(">I", blob, 0)[0]
    out["superblob_magic"] = hex(magic)
    if magic != 0xFADE0CC0:
        out["notes"].append("not a CSSuperBlob")
        return out
    length, count = struct.unpack_from(">II", blob, 4)
    slot_names = {0x00000: "CodeDirectory", 0x00001: "InfoSlot",
                  0x00002: "Requirements", 0x00003: "ResourceDir",
                  0x00004: "Application", 0x00005: "Entitlements",
                  0x00007: "DEREntitlements", 0x0000A: "RepSpecific",
                  0x01000: "AlternateCodeDirectory", 0x10000: "CMSSignature"}
    for i in range(min(count, 32)):
        p = 12 + i * 8
        if p + 8 > len(blob):
            break
        stype, soff = struct.unpack_from(">II", blob, p)
        entry = {"slot": slot_names.get(stype, hex(stype)), "slot_id": hex(stype),
                 "offset": soff}
        if soff + 8 <= len(blob):
            bmagic = struct.unpack_from(">I", blob, soff)[0]
            entry["blob_magic"] = hex(bmagic)
            if bmagic == 0xFADE0C02:  # CodeDirectory
                # 存在两种布局：标准 CodeDirectory，以及本地重签工具常见的
                # 「magic + length + 标准字段」变体。按 version 合法区间自动判别，
                # 判别不了就只记录 magic，绝不套用错误偏移产出伪数据。
                try:
                    v_std = struct.unpack_from(">I", blob, soff + 4)[0]
                    v_var = struct.unpack_from(">I", blob, soff + 8)[0]
                    valid = lambda v: 0x20000 <= v <= 0x2FFFF
                    if valid(v_std):
                        layout, m = "standard", {
                            "version": 4, "flags": 8, "hash_offset": 12,
                            "ident_offset": 16, "n_special": 20, "n_code": 24,
                            "code_limit": 28, "bytes": 32, "team_offset": 44}
                    elif valid(v_var):
                        layout, m = "length-prefixed", {
                            "version": 8, "flags": 12, "hash_offset": 16,
                            "ident_offset": 20, "n_special": 24, "n_code": 28,
                            "code_limit": 32, "bytes": 36, "team_offset": 48}
                    else:
                        layout, m = "unknown", None
                    entry["code_directory_layout"] = layout
                    if m:
                        rd = lambda k: struct.unpack_from(">I", blob, soff + m[k])[0]
                        hsize, htype, plat, psize = blob[soff + m["bytes"]:soff + m["bytes"] + 4]
                        ident_off = rd("ident_offset")
                        team_off = rd("team_offset")
                        entry["code_directory"] = {
                            "version": hex(rd("version")), "flags": hex(rd("flags")),
                            "hash_offset": rd("hash_offset"),
                            "code_slots": rd("n_code"), "special_slots": rd("n_special"),
                            "code_limit": rd("code_limit"),
                            "hash_size": hsize,
                            "hash_type": {1: "SHA-1", 2: "SHA-256", 3: "SHA-384",
                                         4: "SHA-512"}.get(htype, str(htype)),
                            "platform": plat,
                            "page_size": (1 << psize) if psize < 32 else psize,
                            "identifier": cstr(blob, soff + ident_off, len(blob))
                            if ident_off else "",
                            "team_id": cstr(blob, soff + team_off, len(blob))
                            if team_off else "",
                        }
                    else:
                        entry["notes"] = ["CodeDirectory version 不在可识别区间，字段未解析"]
                except (struct.error, IndexError) as exc:
                    entry["code_directory_error"] = str(exc)
            elif bmagic in (0xFADE7171, 0xFADE7172):  # entitlements XML / DER
                try:
                    blen = struct.unpack_from(">I", blob, soff + 4)[0]
                    xml = blob[soff + 8:soff + min(blen, len(blob) - soff)]
                    if bmagic == 0xFADE7171:
                        ent = plistlib.loads(xml) if xml else {}
                        out["entitlements"] = {k: str(v)[:200] for k, v in ent.items()} if isinstance(ent, dict) else {}
                        entry["entitlement_keys"] = sorted(out["entitlements"].keys())
                except Exception as exc:
                    entry["entitlement_error"] = str(exc)
        out["blobs"].append(entry)
    return out


def parse_export_trie(d, base, info):
    off = info["offset"] - base if info["offset"] >= base else info["offset"]
    size = min(info["size"], max(0, len(d) - off))
    out = {"offset": info["offset"], "size": info["size"]}
    if off < 0 or size <= 0:
        return out
    buf = d[off:off + size]
    visited = set()
    terminals = 0
    samples = []

    def walk(node_off, prefix, depth):
        nonlocal terminals
        if depth > 64 or node_off in visited or node_off >= len(buf):
            return
        visited.add(node_off)
        p = node_off
        tsize, p = uleb(buf, p, len(buf))
        if tsize is None:
            return
        p += tsize  # terminal info
        if tsize:
            terminals += 1
            if len(samples) < 10 and prefix:
                samples.append(prefix)
        if p >= len(buf):
            return
        child_count = buf[p]
        p += 1
        for _ in range(min(child_count, 256)):
            end = buf.find(b"\x00", p, len(buf))
            if end < 0:
                return
            edge = buf[p:end].decode("utf-8", "replace")
            p = end + 1
            child, p = uleb(buf, p, len(buf))
            if child is None:
                return
            walk(child, prefix + edge, depth + 1)

    walk(0, "", 0)
    out.update({
        "trie_nodes_visited": len(visited),
        "exported_symbol_count": terminals,
        "sample_export_prefixes": samples,
        "symbol_names_retained": False,
    })
    return out


def classify_dylibs(dylibs):
    groups = {"system_frameworks": [], "system_libs": [], "embedded": [],
              "third_party": [], "swift_runtime": []}
    for item in dylibs:
        n = item["name"]
        low = n.lower()
        if "libswift" in low:
            groups["swift_runtime"].append(n)
        elif n.startswith("/System/Library/") or n.startswith("/usr/lib/"):
            (groups["system_frameworks"] if ".framework/" in n else groups["system_libs"]).append(n)
        elif n.startswith("@rpath/") or n.startswith("@executable_path/") or n.startswith("@loader_path/"):
            groups["embedded"].append(n)
        else:
            groups["third_party"].append(n)
    return {k: {"count": len(v), "items": v} for k, v in groups.items()}


def infer_stack(slice_info):
    hints = []
    objc = slice_info.get("objc", {})
    swift = slice_info.get("swift", {})
    sym = slice_info.get("symbols", {})
    groups = slice_info.get("dylib_groups", {})
    if objc.get("classname_count", 0) > 0 or sym.get("class_count", 0) > 0:
        hints.append("Objective-C（__objc_* 元数据节 + ObjC 类符号）")
    if swift.get("section_count", 0) > 0 or sym.get("category_counts", {}).get("swift_mangled", 0) > 0 \
            or groups.get("swift_runtime", {}).get("count", 0) > 0:
        hints.append("Swift（__swift5_* 节 / Swift mangled 符号 / libswift 运行时）")
    if sym.get("category_counts", {}).get("cpp_mangled", 0) > 0:
        hints.append("C/C++（Itanium mangled 符号）")
    names = " ".join(d["name"] for d in slice_info.get("dylibs", []))
    section_names = " ".join(s["name"] for s in slice_info.get("sections", []))
    for marker, label in [("Flutter", "Flutter"), ("React", "React Native"),
                          ("hermes", "Hermes JS 引擎"), ("JavaScriptCore", "JavaScriptCore"),
                          ("Unity", "Unity"), ("Weex", "Weex"), ("llvm", "LLVM 相关运行时")]:
        if marker.lower() in names.lower():
            hints.append(label + "（依赖库线索）")
    if "__cstring" in section_names:
        hints.append("原生编译产物（__cstring 等静态字符串节）")
    return {"hints": hints, "basis": "静态节名 / 符号前缀 / 依赖库路径，仅为线索，不代表运行时行为"}


def inspect(path):
    report = {
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(),
        "input": os.path.abspath(path),
        "size": os.path.getsize(path),
        "sha256": sha256_of(path),
        "app": {},
        "bundle": {},
        "macho": {},
        "notes": [],
    }
    data = None
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
            info_name = next((n for n in names if n.endswith(".app/Info.plist")), None)
            exe_name = None
            if info_name:
                try:
                    info = plistlib.loads(zf.read(info_name))
                except Exception as exc:
                    info = {}
                    report["notes"].append(f"Info.plist parse failed: {exc}")
                keys = ["CFBundleIdentifier", "CFBundleExecutable",
                        "CFBundleShortVersionString", "CFBundleVersion",
                        "MinimumOSVersion", "CFBundleSupportedPlatforms",
                        "UIDeviceFamily", "ITSAppUsesNonExemptEncryption",
                        "NSAppTransportSecurity", "CFBundleURLTypes",
                        "UIRequiredDeviceCapabilities", "LSRequiresIPhoneOS",
                        "NSCameraUsageDescription", "NSPhotoLibraryUsageDescription",
                        "NSMicrophoneUsageDescription"]
                report["app"] = {k: info.get(k) for k in keys if k in info}
                exe = info.get("CFBundleExecutable")
                if exe:
                    exe_name = info_name[:-len("Info.plist")] + exe
            if exe_name and exe_name in names:
                report["app"]["executable"] = exe_name
                data = zf.read(exe_name)
                report["app"]["executable_size"] = len(data)
            else:
                report["notes"].append("main executable not found in archive")
            exts = Counter(os.path.splitext(n)[1].lower() or "(no ext)" for n in names)
            frameworks = sorted({m.group(1) for n in names
                                 for m in [re.search(r"([^/]+\.framework)/", n)] if m})
            dylibs = sorted({n for n in names if n.endswith(".dylib")})
            plugins = sorted({m.group(1) for n in names
                              for m in [re.search(r"([^/]+\.appex)/", n)] if m})
            report["bundle"] = {
                "entry_count": len(names),
                "extension_histogram": dict(exts.most_common(24)),
                "embedded_frameworks": frameworks,
                "embedded_dylibs": dylibs,
                "app_extensions": plugins,
                "has_mobileprovision": any(n.endswith("embedded.mobileprovision") for n in names),
                "has_code_signature_dir": any("_CodeSignature/" in n for n in names),
                "has_privacy_manifest": any(n.endswith("PrivacyInfo.xcprivacy") for n in names),
                "has_assets_car": any(n.endswith("Assets.car") for n in names),
                "has_nib_or_storyboard": any(n.endswith((".nib", ".storyboardc")) for n in names),
            }
    else:
        with open(path, "rb") as fh:
            data = fh.read()
        report["notes"].append("input treated as raw Mach-O")

    if data is None:
        report["notes"].append("no binary data available")
        return report

    magic_be = struct.unpack_from(">I", data, 0)[0] if len(data) >= 4 else 0
    slices = []
    if magic_be in (FAT_MAGIC, FAT_MAGIC_64):
        nfat = struct.unpack_from(">I", data, 4)[0]
        esize = 32 if magic_be == FAT_MAGIC_64 else 20
        container = "FAT64" if magic_be == FAT_MAGIC_64 else "FAT"
        for i in range(min(nfat, 16)):
            o = 8 + i * esize
            if o + esize > len(data):
                break
            if esize == 32:
                cputype, cpusubtype, soff, ssize, align, reserved = struct.unpack_from(">iiQQII", data, o)
            else:
                cputype, cpusubtype, soff, ssize, align = struct.unpack_from(">iiIII", data, o)
            label = f"{CPU_TYPES.get(cputype, hex(cputype))}/0x{cpusubtype:08x}"
            slices.append(parse_slice(data, soff, ssize, label))
    else:
        container = "thin"
        slices.append(parse_slice(data, 0, len(data), "single"))
    report["macho"] = {"container": container, "slices": slices}
    return report


def md_report(r):
    L = ["# iOS 二进制深度静态结构报告", "",
         f"- 生成时间：{r['generated_at']}",
         f"- 输入：`{r['input']}`",
         f"- 大小：{r['size'] / 1024 / 1024:.2f} MiB",
         f"- SHA-256：`{r['sha256']}`", "",
         "> 范围声明：本报告只记录文件内静态结构与公开元数据（架构、节、符号统计、签名、依赖）。",
         "> 不含反编译伪代码，不逐条列出业务类名/方法名，不定位任何业务方法，",
         "> 不提供规避技术措施的指引。", ""]

    if r.get("app"):
        L += ["## 1. 应用元数据", "", "| 字段 | 值 |", "| --- | --- |"]
        for k, v in r["app"].items():
            t = str(v).replace("|", "\\|").replace("\n", " ")
            L.append(f"| `{k}` | {t[:180]}{' ...' if len(t) > 180 else ''} |")
        L.append("")

    b = r.get("bundle") or {}
    if b:
        L += ["## 2. 包内容分布", "",
              f"- IPA 条目数：**{b.get('entry_count', 0)}**",
              f"- 内嵌 framework：**{len(b.get('embedded_frameworks', []))}** 个；内嵌 dylib：**{len(b.get('embedded_dylibs', []))}** 个",
              f"- App Extension：**{len(b.get('app_extensions', []))}** 个 {b.get('app_extensions', [])}",
              f"- 描述文件：{'有' if b.get('has_mobileprovision') else '无'}／代码签名目录：{'有' if b.get('has_code_signature_dir') else '无'}／隐私清单：{'有' if b.get('has_privacy_manifest') else '无'}",
              f"- Assets.car：{'有' if b.get('has_assets_car') else '无'}／编译 nib/storyboard：{'有' if b.get('has_nib_or_storyboard') else '无'}", ""]
        if b.get("embedded_frameworks"):
            L += ["<details><summary>内嵌 framework 清单</summary>", ""]
            L += [f"- `{x}`" for x in b["embedded_frameworks"]]
            L += ["", "</details>", ""]
        L += ["### 文件类型分布（前 14）", "", "| 扩展名 | 数量 |", "| --- | ---: |"]
        for ext, n in list(b.get("extension_histogram", {}).items())[:14]:
            L.append(f"| `{ext}` | {n} |")
        L.append("")

    m = r.get("macho") or {}
    L += [f"## 3. Mach-O 内部结构（容器：{m.get('container', 'n/a')}）", ""]
    for s in m.get("slices", []):
        if s.get("notes"):
            L += [f"> 解析提示：{'；'.join(s['notes'])}", ""]
        L += [f"### 切片 {s.get('arch_label')}", "",
              f"- CPU：`{s.get('cpu_type')}` / 子类型 `{s.get('cpu_subtype')}` / 类型 `{s.get('filetype')}`",
              f"- 加载命令 **{s.get('ncmds')}** 条（{s.get('sizeofcmds')} 字节）；标志：{', '.join(s.get('flags', [])) or '—'}",
              f"- UUID：`{s.get('uuid') or '未声明'}`；构建：`{s.get('build_version') or '未声明'}`",
              f"- 加密：`{(s.get('encryption') or {}).get('state', '未声明')}`；PIE：**{'是' if s.get('pie') else '否'}**", ""]

        cmds = Counter(c["name"] for c in s.get("load_commands", []))
        L += ["**加载命令构成**", "", "| 命令 | 条数 |", "| --- | ---: |"]
        for k, v in cmds.most_common():
            L.append(f"| `{k}` | {v} |")
        L.append("")

        if s.get("segments"):
            L += ["**段表**", "", "| 段 | VM 大小 | 文件偏移 | 文件大小 | 节数 | 初始保护 |",
                  "| --- | ---: | ---: | ---: | ---: | ---: |"]
            for seg in s["segments"]:
                L.append(f"| `{seg['name']}` | {seg['vmsize']:,} | {seg['fileoff']:,} | "
                         f"{seg['filesize']:,} | {seg['nsects']} | {seg['initprot']} |")
            L.append("")

        secs = s.get("sections", [])
        L += [f"**节表**：共 {len(secs)} 节", ""]
        big = sorted(secs, key=lambda x: -x["size"])[:14]
        L += ["| 段,节 | 大小 | 地址 |", "| --- | ---: | --- |"]
        for x in big:
            L.append(f"| `{x['segment']},{x['name']}` | {x['size']:,} | `{x['addr']}` |")
        L.append("")

        sym = s.get("symbols") or {}
        if sym:
            L += ["**符号表**", "",
                  f"- 符号总数：**{sum(sym.get('type_counts', {}).values()):,}**；ObjC 类符号：**{sym.get('class_count', 0):,}**", ""]
            L += ["| 符号类型 | 数量 |", "| --- | ---: |"]
            for k, v in sorted(sym.get("type_counts", {}).items(), key=lambda kv: -kv[1]):
                L.append(f"| `{k}` | {v:,} |")
            L += [""]
            if sym.get("category_counts"):
                L += ["| 符号归类 | 数量 |", "| --- | ---: |"]
                for k, v in sorted(sym["category_counts"].items(), key=lambda kv: -kv[1]):
                    L.append(f"| `{k}` | {v:,} |")
                L += [""]
            if sym.get("prefix_histogram"):
                L += ["类符号前缀聚类（仅统计，不输出业务类名）：" +
                      "、".join(f"`{k}`({v})" for k, v in list(sym["prefix_histogram"].items())[:14]), ""]

        ob = s.get("objc") or {}
        sw = s.get("swift") or {}
        L += ["**Objective-C / Swift 元数据**", "",
              "| 指标 | 值 |", "| --- | ---: |",
              f"| `__objc_*` 节数 | {len(ob.get('present_sections', {}))} |",
              f"| 类名字符串数 | {ob.get('classname_count', 0):,} |",
              f"| 方法名字符串数 | {ob.get('methname_count', 0):,} |",
              f"| classlist 条目 | {ob.get('classlist_entries', 0):,} |",
              f"| selector 引用 | {ob.get('selector_refs', 0):,} |",
              f"| class 引用 | {ob.get('class_refs', 0):,} |",
              f"| category / protocol | {ob.get('category_entries', 0):,} / {ob.get('protocol_entries', 0):,} |",
              f"| Swift `__swift5_*` 节数 | {sw.get('section_count', 0)} |", ""]
        if ob.get("present_sections"):
            L += ["<details><summary>ObjC 节及大小</summary>", ""]
            for k, v in sorted(ob["present_sections"].items()):
                L.append(f"- `{k}` — {v['size']:,} B")
            L += ["", "</details>", ""]

        st = s.get("strings") or {}
        if st.get("sections"):
            L += ["**静态字符串节**", "", "| 节 | 大小 | 字符串数 | 平均长度 | 最长 |",
                  "| --- | ---: | ---: | ---: | ---: |"]
            for k, v in st["sections"].items():
                L.append(f"| `{k}` | {v['size']:,} | {v.get('string_count', '—')} | "
                         f"{v.get('avg_len', '—')} | {v.get('max_len', '—')} |")
            L.append("")

        sig = s.get("signature") or {}
        if sig.get("blobs"):
            L += ["**代码签名**", "",
                  f"- SuperBlob：`{sig.get('superblob_magic')}`；blob 数 {len(sig['blobs'])}", ""]
            for e in sig["blobs"]:
                cd = e.get("code_directory")
                line = f"- `{e['slot']}`（{e.get('blob_magic')}）"
                if cd:
                    line += (f"：标识 `{cd.get('identifier')}`，{cd.get('hash_type')}，"
                             f"page {cd.get('page_size')} B，codeSlots {cd.get('code_slots'):,}，"
                             f"TeamID `{cd.get('team_id') or '未声明'}`，"
                             f"布局 `{e.get('code_directory_layout', '?')}`")
                L.append(line)
            if sig.get("entitlements"):
                L += ["", " entitlements 键：" +
                      "、".join(f"`{k}`" for k in sorted(sig["entitlements"].keys())[:20])]
            L.append("")

        ex = s.get("exports") or {}
        if ex:
            L += ["**导出表（exports trie）**", "",
                  f"- 大小 {ex.get('size', 0):,} B；遍历节点 {ex.get('trie_nodes_visited', 0):,}；"
                  f"导出符号约 **{ex.get('exported_symbol_count', 0):,}** 个（符号名未留存）", ""]

        lk = s.get("linkedit") or {}
        if lk:
            L += ["**LINKEDIT 数据区**", "", "| 区域 | 偏移 | 大小 |", "| --- | ---: | ---: |"]
            for k, v in lk.items():
                L.append(f"| `{k}` | {v['offset']:,} | {v['size']:,} |")
            L.append("")

        dg = s.get("dylib_groups") or {}
        L += ["**依赖库归类**", "", "| 类别 | 数量 |", "| --- | ---: |"]
        for k, v in dg.items():
            L.append(f"| `{k}` | {v['count']} |")
        L.append("")
        if dg.get("embedded", {}).get("items"):
            L += ["<details><summary>内嵌/第三方动态库路径</summary>", ""]
            L += [f"- `{x}`" for x in dg["embedded"]["items"]]
            dg2 = dg.get("third_party", {}).get("items", [])
            L += [f"- `{x}`" for x in dg2]
            L += ["", "</details>", ""]

        if s.get("mechanisms"):
            L += ["**公开技术机制观察**（仅依据符号/节名是否存在，不作绕过推断）", "",
                  "| 类别 | 命中的符号 |", "| --- | --- |"]
            for k, v in s["mechanisms"].items():
                L.append(f"| `{k}` | {', '.join('`' + x + '`' for x in v)} |")
            L.append("")

        si = s.get("stack_inference") or {}
        if si.get("hints"):
            L += ["**技术栈推断**：" + "；".join(si["hints"]), "",
                  f"> {si.get('basis')}", ""]

    if r.get("notes"):
        L += ["## 备注", ""] + [f"- {n}" for n in r["notes"]] + [""]
    L += ["---", "",
          "本报告由只读静态解析生成，用于学习 iOS 二进制组织方式与工程实践；",
          "不包含、也不构成对任何技术措施的规避方法。", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="只读 iOS Mach-O 深度静态结构解析")
    ap.add_argument("target", help="IPA 或 Mach-O 文件路径")
    ap.add_argument("--out", help="报告输出目录")
    a = ap.parse_args()
    if not os.path.isfile(a.target):
        print(f"[!] 文件不存在: {a.target}", file=sys.stderr)
        return 2
    rep = inspect(a.target)
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.target)), "deep-report")
    os.makedirs(out, exist_ok=True)
    stem = re.sub(r"[^A-Za-z0-9_.-]", "_", os.path.splitext(os.path.basename(a.target))[0])
    jp = os.path.join(out, stem + ".deep.json")
    mp = os.path.join(out, stem + ".deep.md")
    with open(jp, "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=2)
    with open(mp, "w", encoding="utf-8") as f:
        f.write(md_report(rep))
    print(f"[+] JSON : {jp}")
    print(f"[+] MD   : {mp}")
    for s in rep.get("macho", {}).get("slices", []):
        print(f"[+] {s['arch_label']}: syms={sum((s.get('symbols') or {}).get('type_counts', {}).values()):,} "
              f"objc_classes={(s.get('objc') or {}).get('classname_count', 0):,} "
              f"exports={(s.get('exports') or {}).get('exported_symbol_count', 0):,} "
              f"enc={(s.get('encryption') or {}).get('state', 'n/a')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
