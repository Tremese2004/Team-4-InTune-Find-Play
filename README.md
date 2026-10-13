# Team-4-InTune-Find-Play
InTune: Find &amp; Play is an app where users can search various songs using voice and/or lyric recognition.

InTune - WINDOWS PYTHON DEMO

1. Extract the ZIP to a folder.
2. Install Python 3 with Tcl/Tk support (standard Windows installer).
3. Double-click Start_Demo.bat.
   Or run: py -3 song_detector.py

No pip packages, API keys, or music accounts are needed.

PRESENTATION WALKTHROUGH (about 30 seconds)
1. Show the detector window.
2. Click Detect demo song. The bars animate and the progress bar fills.
3. A separate song result window opens and the detector window hides.
4. Click Search on Spotify or Search on Apple Music to open a browser search.
5. Click Back to detector to return to the first window.
6. Click Detect demo song again to demonstrate repeat navigation.

Closing the result window also returns to the detector.
Closing the detector exits the app.

SCOPE
This is a UI prototype. It does not record audio, recognize real songs,
authenticate accounts, play audio, or call Spotify/Apple Music APIs.
The fixed sample result is Blinding Lights by The Weeknd.
Music buttons open public browser searches only.

Validation: Python syntax compilation passed. The build environment had
no desktop display, so an on-screen run could not be recorded here.
