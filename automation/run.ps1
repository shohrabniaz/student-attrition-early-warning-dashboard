$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
if (-not (Test-Path .venv)) { python -m venv .venv }
.\.venv\Scripts\python.exe -m pip install -q -r requirements.txt
.\.venv\Scripts\python.exe -m src.cli run
.\.venv\Scripts\python.exe tests\test_smoke.py
Write-Host 'OK: student-attrition-early-warning-dashboard'
