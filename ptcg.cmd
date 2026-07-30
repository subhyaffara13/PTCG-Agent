@echo off
cd /d "%~dp0"
if exist "%~dp0%1.py" (
    python %1.py %2 %3 %4 %5 %6 %7 %8 %9
) else (
    python -m %1 %2 %3 %4 %5 %6 %7 %8 %9
)
