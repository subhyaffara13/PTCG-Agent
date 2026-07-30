@echo off
copy /Y "%~dp0run.cmd" "%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\run.cmd"
echo Registered global run command! You can now type run from anywhere.
