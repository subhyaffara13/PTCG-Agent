@echo off
cd /d "%~dp0"
python -m pip install -r "requirements.txt" >nul 2>&1
python -m run %*
:: Or use: ptcg-run %*
