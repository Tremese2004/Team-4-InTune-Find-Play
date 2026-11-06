@echo off
cd /d "%~dp0"
py -3 intune_app.py
if errorlevel 1 pause
