InTune Python Playlist + Library prototype

RUN
1. Install Python 3 on Windows.
2. Open this folder in File Explorer.
3. Double-click run_intune.bat, or run: python intune_app.py

WHAT WORKS
- Library screen with Recent Saves, Recent Plays, Favorites, and My Playlists.
- Create playlists and open them.
- Rename playlists.
- Add songs from the sample catalog.
- Search within a playlist or across the sample catalog.
- Play a selected song in the mini-player (UI state only; no audio playback).
- Save songs to the library, favorite/unfavorite, and remove songs from a playlist.
- Bottom navigation between Home, Search, Library, and Playlist.

PROJECT CONTEXT
The supplied GitHub ZIP is mixed:
- demo.py is a Python Tkinter song-detector prototype.
- music_search_screen.py is Flutter/Dart source code despite its .py filename.
- README.md describes a Python desktop demo.
This implementation follows the Python/Tkinter direction and is a separate runnable app entry point.
It does not overwrite demo.py or the existing music_search_screen.py.

LIMITATIONS
Song data is sample data and all changes are in memory; they reset when the app closes.
The mini-player is a UI prototype and does not play audio.
