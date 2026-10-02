<#
.SYNOPSIS
    Asks for your Kaggle Jupyter-server link, then starts the backend, connects the Kaggle GPU
    session and opens the UI. Finished videos are saved to the output drive (J:).

.DESCRIPTION
    Works with Windows PowerShell 5.1 and PowerShell 7.
    Run from the "valid models" folder:

        powershell -ExecutionPolicy Bypass -File .\Start-Kaggle.ps1
        powershell -ExecutionPolicy Bypass -File .\Start-Kaggle.ps1 -Gradio -OpenVSCode

    The link (https://....kaggle.net/k/<id>/<token>/proxy) contains a live access token to your
    Kaggle session, so it is read as hidden input, handed to Python through an environment
    variable (not the command line, which other programs can see), and cleared afterwards.

.PARAMETER Gradio
    Also open a Gradio viewer for the finished videos (http://127.0.0.1:7860).
.PARAMETER OpenVSCode
    Also open this project folder in your local VS Code.
.PARAMETER NoBrowser
    Do not open the browser automatically.
.PARAMETER InstallMissing
    Install missing Python packages without asking.
#>
[CmdletBinding()]
param(
    [string]$ProjectDir = $PSScriptRoot,
    [switch]$Gradio,
    [switch]$OpenVSCode,
    [switch]$NoBrowser,
    [switch]$InstallMissing
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Find-Python {
    # Returns @(exe, extra args...) for the first Python >= 3.9 that works. Skips the Microsoft Store stub.
    $candidates = @(
        @{ Exe = 'py';      Args = @('-3') },
        @{ Exe = 'python';  Args = @() },
        @{ Exe = 'python3'; Args = @() }
    )
    foreach ($c in $candidates) {
        if (-not (Get-Command $c.Exe -ErrorAction SilentlyContinue)) { continue }
        try {
            $ok = & $c.Exe @($c.Args) -c "import sys; print(sys.version_info >= (3, 9))" 2>$null
            if ("$ok".Trim() -eq 'True') { return @($c.Exe) + @($c.Args) }
        } catch { }
    }
    throw "Python 3.9 or newer was not found. Install it from https://www.python.org/downloads/ and tick 'Add python.exe to PATH'."
}

function Read-KaggleLink {
    if ($env:KAGGLE_JUPYTER_URL) {
        Write-Host 'Using the link from the KAGGLE_JUPYTER_URL environment variable.'
        return $env:KAGGLE_JUPYTER_URL.Trim()
    }
    Write-Host ''
    Write-Host 'In your Kaggle notebook, copy the Jupyter-server link' -ForegroundColor Cyan
    Write-Host '(it looks like https://....jupyter-proxy.kaggle.net/k/<id>/<token>/proxy).'
    $secure = Read-Host 'Paste the link (input is hidden)' -AsSecureString
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try { return ([Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)).Trim().Trim('"', "'") }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
}

# ---- checks ---------------------------------------------------------------------------------
$ProjectDir = (Resolve-Path -LiteralPath $ProjectDir).Path
$runAll = Join-Path $ProjectDir 'run_all.py'
if (-not (Test-Path -LiteralPath $runAll)) {
    throw "run_all.py was not found in '$ProjectDir'. Run this script from the 'valid models' folder."
}

$py = @(Find-Python)          # @() keeps it an array even when it holds a single element
$pyExe = $py[0]
$pyArgs = @()
if ($py.Count -gt 1) { $pyArgs = $py[1..($py.Count - 1)] }
Write-Host ("Python: " + (& $pyExe @pyArgs --version))

$link = Read-KaggleLink
if ($link -notmatch '^https://[A-Za-z0-9.-]+\.kaggle\.net/\S+$') {
    throw "That does not look like a Kaggle link. Expected https://<host>.kaggle.net/k/<id>/<token>/proxy"
}
if ($link -match '\s') { throw 'The link must not contain spaces or line breaks.' }

if ($OpenVSCode -and (Get-Command code -ErrorAction SilentlyContinue)) {
    & code $ProjectDir | Out-Null
} elseif ($OpenVSCode) {
    Write-Warning "VS Code ('code' command) was not found on PATH; skipping."
}

# ---- run ------------------------------------------------------------------------------------
$extra = @('--kaggle')
if ($Gradio)         { $extra += '--gradio' }
if ($NoBrowser)      { $extra += '--no-browser' }
if ($InstallMissing) { $extra += '--install' }

Push-Location $ProjectDir
try {
    $env:KAGGLE_JUPYTER_URL = $link      # read by run_all.py, removed from every child process
    $link = $null
    & $pyExe @pyArgs $runAll @extra
    if ($LASTEXITCODE -ne 0) { Write-Warning "run_all.py exited with code $LASTEXITCODE" }
}
finally {
    Remove-Item Env:KAGGLE_JUPYTER_URL -ErrorAction SilentlyContinue
    Pop-Location
}
