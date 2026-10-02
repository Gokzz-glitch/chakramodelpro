@echo off
rem Double-click launcher: backend + Kaggle GPU + Gradio viewer. Asks for the Kaggle link (visible input: paste works; or it takes the link from the clipboard).
cd /d "%~dp0"
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY (
  echo Python 3.9 or newer was not found. Install it from python.org and tick "Add python.exe to PATH".
  pause
  exit /b 1
)
%PY% run_all.py --kaggle --gradio %*
echo.
pause
