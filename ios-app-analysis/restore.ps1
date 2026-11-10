# iOS 应用结构分析归档 - 分卷合并与 SHA-256 校验（无需 Python）
# 用法: powershell -ExecutionPolicy Bypass -File restore.ps1
#       加 -Download 可自动从 GitHub 下载缺失分卷

param([switch]$Download)

$ErrorActionPreference = "Stop"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Manifest = Join-Path $Here "archive-manifest.json"
$PartsDir = Join-Path $Here "ipa-parts"
$ManifestUrl = "https://raw.githubusercontent.com/Xuefeng122/talang-files/main/ios-app-analysis/archive-manifest.json"
if (-not (Test-Path $Manifest)) {
    Write-Host "archive-manifest.json not found, downloading..."
    Invoke-WebRequest -Uri $ManifestUrl -OutFile $Manifest -UseBasicParsing
}

$m = Get-Content $Manifest -Raw -Encoding UTF8 | ConvertFrom-Json
$base = $m.raw_base
$allOk = $true

foreach ($o in $m.originals) {
    Write-Host ""
    Write-Host "=== $($o.display_name) -> $($o.output) ==="
    $verified = @()
    foreach ($p in $o.parts) {
        $f = Join-Path $PartsDir $p.name
        if (-not (Test-Path $f)) {
            if (-not $Download) {
                Write-Host "  MISSING $($p.name)  (use -Download)"
                $allOk = $false
                continue
            }
            New-Item -ItemType Directory -Force -Path $PartsDir | Out-Null
            $url = $base + "ipa-parts/" + $p.name
            Write-Host "  downloading $url"
            Invoke-WebRequest -Uri $url -OutFile $f -UseBasicParsing
        }
        $actual = (Get-FileHash $f -Algorithm SHA256).Hash.ToLower()
        $size = (Get-Item $f).Length
        if ($actual -ne $p.sha256 -or $size -ne $p.size) {
            Write-Host "  FAIL $($p.name) hash/size mismatch"
            $allOk = $false
            continue
        }
        Write-Host "  OK $($p.name)  $size B"
        $verified += $f
    }
    if (-not $allOk -or $verified.Count -ne $o.parts.Count) {
        Write-Host "  skip merge (missing or damaged parts)"
        continue
    }
    $target = Join-Path $Here $o.output
    $stream = [System.IO.File]::Open($target, "Create", "Write")
    try {
        foreach ($f in $verified) {
            $bytes = [System.IO.File]::ReadAllBytes($f)
            $stream.Write($bytes, 0, $bytes.Length)
        }
    } finally { $stream.Close() }
    $final = (Get-FileHash $target -Algorithm SHA256).Hash.ToLower()
    if ($final -eq $o.sha256) {
        Write-Host "  RESTORED $target  ($($o.size) B)"
    } else {
        Write-Host "  FAIL merged hash mismatch"
        $allOk = $false
    }
}
Write-Host ""
if ($allOk) { Write-Host "All parts verified and restored." } else { Write-Host "Errors found."; exit 1 }
