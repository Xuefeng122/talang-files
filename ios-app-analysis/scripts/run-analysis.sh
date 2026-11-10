#!/usr/bin/env bash
# 对 01-IPA/ 下的所有 IPA 批量做只读结构分析。
# 两层：macho_inspect.py（容器/包层） + deep_inspect.py（二进制内部层）
# 用法（Git Bash）：bash run-analysis.sh
set -u
cd "$(dirname "$0")" || exit 1
OUT="$(pwd)/reports"
DEEP="$(pwd)/target-reports"
mkdir -p "$OUT" "$DEEP"

found=0
for ipa in ../01-IPA/*.ipa; do
  [ -f "$ipa" ] || continue
  found=1
  echo "==> $ipa"
  python macho_inspect.py "$ipa" --out "$OUT"      || echo "[!] 包层解析失败: $ipa"
  python deep_inspect.py "$ipa" --out "$DEEP"     || echo "[!] 深度解析失败: $ipa"
done

if [ "$found" -eq 0 ]; then
  echo "[i] 01-IPA/ 里还没有 IPA 文件，请先归档 Soul 与陌陌的安装包。"
  exit 1
fi

echo "[+] 包层报告目录: $OUT"
echo "[+] 深度报告目录: $DEEP"
ls -1 "$DEEP"
