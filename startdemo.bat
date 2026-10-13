@echo off
cd /d "%~dp0"
py -3 song_detector.py
if errorlevel 1 (
  echo.
  echo If the app did not open, install Python 3 with Tcl/Tk support.
  echo You can also run: python song_detector.py
  pause
)