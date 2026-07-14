@echo off
python -m pip install -r "%~dp0requirements.txt" >nul 2>&1
python "%~dp0run.py" %*
