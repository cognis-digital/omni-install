#requires -version 5
<#
  Cognis guided setup wizard - bootstrap one-liner (stdlib Python only).

    .\setup.ps1            launch the wizard, then type a number
    .\setup.ps1 --dry-run  safe preview: shows commands, runs nothing

  Finds python/python3 and runs the canonical wizard next to this script.
  With no local MANIFEST.json the wizard auto-fetches the cognis-arsenal
  catalog; override with --manifest <path-or-url> or COGNIS_MANIFEST_URL.
#>
$ErrorActionPreference = "Stop"
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$py = $null
foreach ($cand in @("python", "python3", "py")) {
  if (Get-Command $cand -ErrorAction SilentlyContinue) { $py = $cand; break }
}
if (-not $py) { Write-Error "Python 3 is required (python not found on PATH)."; exit 1 }
& $py (Join-Path $dir "cognis_setup.py") @args
exit $LASTEXITCODE
