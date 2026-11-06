"""InTune: Playlist and Library screens (Python/Tkinter prototype).

Run with: python intune_app.py
Uses only Python's standard library. Data is stored in memory for this demo.
"""
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

BG = "#171323"
PANEL = "#211B31"
PURPLE = "#9148F5"
VIOLET = "#713CFF"
CYAN = "#53D9DF"
PINK = "#FF5BB8"
WHITE = "#F7F5FB"
MUTED = "#B8B3C9"
DARK = "#3026A8"

SONG_DATA = [
    ("SET IT OFF", "Offset", 182),
    ("Under The Sun", "Dreamville, J. Cole, DaBaby, Lute", 239),
    ("Bodies", "Offset & JID", 205),
    ("Surround Sound", "JID, 21 Savage, Baby Tate", 229),
    ("Like That", "Future, Metro Boomin", 267),
    ("BUTTERFLY EFFECT", "Travis Scott", 191),
    ("heart pt. 6", "Kendrick Lamar", 250),
    ("Do For Love", "2Pac", 286),
    ("meet the grahams", "Kendrick Lamar", 366),
    ("Can't Tell Me Nothing", "Kanye West", 271),
    ("Have You Ever", "Brandy", 245),
]

class InTuneApp:
    def __init__(self, root):
        self.root = root
        root.title("InTune | Playlist & Library")
        root.geometry("440x850")
        root.minsize(390, 700)
        root.configure(bg=BG)

        self.songs = [
            {"title": t, "artist": a, "seconds": d}
            for t, a, d in SONG_DATA
        ]
        self.playlists = [
            {"name": "Shower Jamz", "emoji": "🧸", "songs": self.songs.copy()},
            {"name": "Gym Set", "emoji": "🐔", "songs": [self.songs[i] for i in (4, 5, 0)]},
            {"name": "Work Mix", "emoji": "🧑‍💻", "songs": [self.songs[i] for i in (6, 8, 10)]},
        ]
        self.library = []
        self.favorites = []
        self.recent_saves = []
        self.recent_plays = []
        self.current_song = None
        self.playing = False
        self.active_playlist = 0
        self.current_screen = "library"
        self.build_shell()
        self.show_library()

    def build_shell(self):
        self.header = tk.Frame(self.root, bg=BG)
        self.header.pack(fill="x", padx=18, pady=(14, 8))
        self.header_title = tk.Label(self.header, text="InTune", bg=BG, fg=PURPLE,
                                     font=("Segoe UI", 21, "bold"))
        self.header_title.pack(side="left")
        tk.Button(self.header, text="●", command=self.show_profile, bg=BG, fg=PINK,
                  activebackground=BG, relief="flat", font=("Segoe UI", 18, "bold")).pack(side="right")

        self.content = tk.Frame(self.root, bg=BG)
        self.content.pack(fill="both", expand=True, padx=16)

        self.player = tk.Frame(self.root, bg="#332A45", height=58)
        self.player.pack(fill="x", side="bottom")
        self.player.pack_propagate(False)
        self.player_label = tk.Label(self.player, text="No song selected", bg="#332A45",
                                     fg=WHITE, anchor="w", font=("Segoe UI", 9, "bold"))
        self.player_label.pack(side="left", fill="x", expand=True, padx=10)
        self.play_button = tk.Button(self.player, text="▶", command=self.toggle_play,
                                     bg="#332A45", fg=WHITE, relief="flat", font=("Segoe UI", 14))
        self.play_button.pack(side="right", padx=5)
        tk.Button(self.player, text="▶▶", command=self.next_song, bg="#332A45",
                  fg=WHITE, relief="flat").pack(side="right", padx=5)

        self.nav = tk.Frame(self.root, bg=PANEL)
        self.nav.pack(side="bottom", fill="x")
        for label, screen in [("⌂  Home", "home"), ("⌕  Search", "search"),
                              ("♧  Library", "library"), ("♫  Playlist", "playlist")]:
            tk.Button(self.nav, text=label, command=lambda s=screen: self.navigate(s),
                      bg=PANEL, fg=WHITE, activebackground=PURPLE, activeforeground=WHITE,
                      relief="flat", font=("Segoe UI", 10), padx=8, pady=11).pack(
                          side="left", expand=True, fill="x")

    def clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()

    def heading(self, title, action_text=None, action=None):
        bar = tk.Frame(self.content, bg=BG)
        bar.pack(fill="x", pady=(5, 12))
        tk.Label(bar, text=title, bg=BG, fg=WHITE,
                 font=("Segoe UI", 18, "bold")).pack(side="left")
        if action_text:
            tk.Button(bar, text=action_text, command=action, bg=BG, fg=PINK,
                      activebackground=BG, relief="flat",
                      font=("Segoe UI", 10, "bold")).pack(side="right")

    def show_library(self):
        self.current_screen = "library"
        self.clear_content()
        self.heading("Library", "+", self.create_playlist)

        search = tk.Button(self.content, text="▥     SEARCH HISTORY", command=self.search_all,
                           bg="#F0EFF2", fg="#171323", relief="flat",
                           font=("Segoe UI", 10, "bold"), pady=9)
        search.pack(fill="x", pady=(0, 15))

        self.feature_card("▣", "Recent Saves", self.recent_saves)
        self.feature_card("▣", "Recent Plays", self.recent_plays)
        self.feature_card("♥", "Favorites", self.favorites, heart=True)

        line = tk.Frame(self.content, bg=BG)
        line.pack(fill="x", pady=(9, 7))
        tk.Frame(line, bg=VIOLET, height=1).pack(side="left", fill="x", expand=True, pady=12)
        tk.Label(line, text=" My Playlists ", bg=BG, fg=VIOLET,
                 font=("Segoe UI", 14, "bold")).pack(side="left")
        tk.Frame(line, bg=VIOLET, height=1).pack(side="left", fill="x", expand=True, pady=12)

        list_frame = tk.Frame(self.content, bg=BG)
        list_frame.pack(fill="both", expand=True)
        for index, playlist in enumerate(self.playlists):
            row = tk.Frame(list_frame, bg=PURPLE, highlightbackground=VIOLET, highlightthickness=2)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=playlist["emoji"], bg=VIOLET, fg=WHITE,
                     font=("Segoe UI Emoji", 22), width=3, pady=5).pack(side="left", padx=4, pady=4)
            tk.Button(row, text=playlist["name"], command=lambda i=index: self.open_playlist(i),
                      bg=PURPLE, fg=WHITE, activebackground=PURPLE, relief="flat",
                      anchor="w", font=("Segoe UI", 12, "bold")).pack(side="left", fill="x", expand=True)
            tk.Label(row, text=str(len(playlist["songs"])), bg=PURPLE, fg=WHITE,
                     font=("Segoe UI", 10)).pack(side="right", padx=10)

        if self.library:
            tk.Label(self.content, text="Saved to Library", bg=BG, fg=WHITE,
                     font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(12, 4))
            self.song_list(self.library, self.content, compact=True)

    def feature_card(self, icon, title, items, heart=False):
        color = PURPLE
        row = tk.Frame(self.content, bg=color, highlightbackground=VIOLET, highlightthickness=2)
        row.pack(fill="x", pady=5)
        tk.Button(row, text=icon, command=lambda: self.show_collection(title, items),
                  bg=color, fg="#FF4F62" if heart else DARK, relief="flat",
                  font=("Segoe UI", 26, "bold"), width=3).pack(side="left", padx=4, pady=6)
        tk.Button(row, text=title, command=lambda: self.show_collection(title, items),
                  bg=color, fg="#FFD4EA" if heart else DARK, relief="flat",
                  font=("Segoe UI", 17, "bold"), anchor="w").pack(side="left", fill="x", expand=True)
        tk.Label(row, text=str(len(items)), bg=color, fg=WHITE).pack(side="right", padx=10)

    def show_collection(self, title, items):
        self.clear_content()
        self.heading(title, "← Library", self.show_library)
        if not items:
            tk.Label(self.content, text="Nothing here yet. Play or save songs to populate this section.",
                     bg=BG, fg=MUTED, wraplength=340).pack(pady=30)
        else:
            self.song_list(items, self.content)

    def open_playlist(self, index):
        self.active_playlist = index
        self.show_playlist()

    def show_playlist(self):
        self.current_screen = "playlist"
        self.clear_content()
        playlist = self.playlists[self.active_playlist]
        self.heading(playlist["name"], "EDIT", self.rename_playlist)

        search_var = tk.StringVar()
        search_box = tk.Frame(self.content, bg="#F0EFF2")
        search_box.pack(fill="x", pady=(0, 12))
        tk.Label(search_box, text="⌕", bg="#F0EFF2", fg="#171323",
                 font=("Segoe UI", 15)).pack(side="left", padx=8)
        entry = tk.Entry(search_box, textvariable=search_var, bg="#F0EFF2", fg="#171323",
                         relief="flat", font=("Segoe UI", 10))
        entry.pack(side="left", fill="x", expand=True, ipady=8)
        tk.Button(search_box, text="×", command=lambda: search_var.set(""),
                  bg="#F0EFF2", fg="#171323", relief="flat").pack(side="right", padx=6)

        total = sum(song["seconds"] for song in playlist["songs"])
        stats = tk.Frame(self.content, bg=BG)
        stats.pack(fill="x", pady=(0, 10))
        for value, label in [(f"💿\n{len(playlist['songs'])}", "Track Count"),
                             (f"{playlist['emoji']}\n{playlist['name']}", "Playlist"),
                             (f"⌛\n{total // 3600}h {(total % 3600) // 60}m", "Playlist Span")]:
            block = tk.Frame(stats, bg=BG)
            block.pack(side="left", expand=True)
            tk.Label(block, text=value, bg=BG, fg=WHITE, font=("Segoe UI", 12, "bold"),
                     wraplength=120).pack()
            tk.Label(block, text=label, bg=BG, fg=CYAN,
                     font=("Segoe UI", 9, "bold")).pack()

        controls = tk.Frame(self.content, bg=BG)
        controls.pack(fill="x", pady=(0, 6))
        tk.Button(controls, text="+ Add Songs", command=self.add_songs, bg=VIOLET,
                  fg=WHITE, relief="flat", padx=10, pady=5).pack(side="left")
        tk.Button(controls, text="Back to Library", command=self.show_library,
                  bg=PANEL, fg=WHITE, relief="flat", padx=10, pady=5).pack(side="right")

        holder = tk.Frame(self.content, bg=BG)
        holder.pack(fill="both", expand=True)

        def refresh(*_):
            for child in holder.winfo_children():
                child.destroy()
            query = search_var.get().lower().strip()
            visible = [s for s in playlist["songs"]
                       if query in s["title"].lower() or query in s["artist"].lower()]
            if not visible:
                tk.Label(holder, text="No matching songs.", bg=BG, fg=MUTED).pack(pady=25)
            else:
                self.song_list(visible, holder, playlist=playlist)
        search_var.trace_add("write", refresh)
        refresh()

    def song_list(self, songs, parent, compact=False, playlist=None):
        for song in songs:
            row = tk.Frame(parent, bg=CYAN, highlightbackground=VIOLET, highlightthickness=1)
            row.pack(fill="x", pady=3)
            tk.Label(row, text="♫", bg="#332A70", fg=WHITE, width=3,
                     font=("Segoe UI", 15)).pack(side="left", padx=4, pady=4)
            details = tk.Frame(row, bg=CYAN)
            details.pack(side="left", fill="x", expand=True, padx=3, pady=4)
            tk.Button(details, text=song["title"], command=lambda s=song: self.play_song(s),
                      bg=CYAN, fg=WHITE, relief="flat", anchor="w",
                      font=("Segoe UI", 9, "bold")).pack(fill="x")
            tk.Label(details, text=song["artist"], bg=CYAN, fg="#EAFBFF",
                     anchor="w", font=("Segoe UI", 8)).pack(fill="x")
            menu = tk.Menubutton(row, text="⋮", bg=CYAN, fg=WHITE, relief="flat")
            menu.pack(side="right", padx=4)
            popup = tk.Menu(menu, tearoff=0)
            popup.add_command(label="Play", command=lambda s=song: self.play_song(s))
            popup.add_command(label="Save to Library", command=lambda s=song: self.save_song(s))
            popup.add_command(label="Add / remove Favorite", command=lambda s=song: self.toggle_favorite(s))
            if playlist is not None:
                popup.add_command(label="Remove from Playlist",
                                  command=lambda s=song, p=playlist: self.remove_song(p, s))
            menu.configure(menu=popup)

    def create_playlist(self):
        name = simpledialog.askstring("Create Playlist", "Enter a playlist name:", parent=self.root)
        if name and name.strip():
            self.playlists.append({"name": name.strip(), "emoji": "🎵", "songs": []})
            self.active_playlist = len(self.playlists) - 1
            self.show_playlist()

    def rename_playlist(self):
        playlist = self.playlists[self.active_playlist]
        name = simpledialog.askstring("Rename Playlist", "New playlist name:",
                                      initialvalue=playlist["name"], parent=self.root)
        if name and name.strip():
            playlist["name"] = name.strip()
            self.show_playlist()

    def add_songs(self):
        playlist = self.playlists[self.active_playlist]
        win = tk.Toplevel(self.root)
        win.title("Add songs")
        win.configure(bg=BG)
        win.geometry("390x500")
        tk.Label(win, text="Choose songs to add", bg=BG, fg=WHITE,
                 font=("Segoe UI", 15, "bold")).pack(pady=12)
        selected = []
        area = tk.Frame(win, bg=BG)
        area.pack(fill="both", expand=True, padx=12)
        for song in self.songs:
            var = tk.BooleanVar(value=song in playlist["songs"])
            cb = tk.Checkbutton(area, text=f'{song["title"]} — {song["artist"]}',
                                variable=var, state="disabled" if song in playlist["songs"] else "normal",
                                bg=BG, fg=WHITE, selectcolor=PANEL, activebackground=BG,
                                wraplength=330, anchor="w", justify="left")
            cb.pack(fill="x", anchor="w")
            selected.append((song, var))
        def add_selected():
            additions = [song for song, var in selected if var.get() and song not in playlist["songs"]]
            playlist["songs"].extend(additions)
            win.destroy()
            self.show_playlist()
        tk.Button(win, text="Add Selected", command=add_selected, bg=PURPLE,
                  fg=WHITE, relief="flat", pady=9).pack(fill="x", padx=18, pady=14)

    def remove_song(self, playlist, song):
        if song in playlist["songs"]:
            playlist["songs"].remove(song)
        self.show_playlist()

    def save_song(self, song):
        if song not in self.library:
            self.library.append(song)
            self.recent_saves.insert(0, song)
            self.recent_saves = self.recent_saves[:10]
            messagebox.showinfo("InTune", "Song saved to your library.")
        else:
            messagebox.showinfo("InTune", "This song is already in your library.")
        if self.current_screen == "library":
            self.show_library()

    def toggle_favorite(self, song):
        if song in self.favorites:
            self.favorites.remove(song)
        else:
            self.favorites.append(song)
        messagebox.showinfo("Favorites", "Favorites updated.")

    def play_song(self, song):
        self.current_song = song
        self.playing = True
        self.recent_plays = [song] + [s for s in self.recent_plays if s != song]
        self.recent_plays = self.recent_plays[:10]
        self.update_player()

    def update_player(self):
        if self.current_song:
            self.player_label.config(text=f'{self.current_song["title"]}  •  {self.current_song["artist"]}')
        self.play_button.config(text="Ⅱ" if self.playing else "▶")

    def toggle_play(self):
        if self.current_song:
            self.playing = not self.playing
            self.update_player()

    def next_song(self):
        if not self.current_song:
            return
        index = self.songs.index(self.current_song)
        self.play_song(self.songs[(index + 1) % len(self.songs)])

    def search_all(self):
        self.current_screen = "search"
        self.clear_content()
        self.heading("Search Music", "← Library", self.show_library)
        query = tk.StringVar()
        entry = tk.Entry(self.content, textvariable=query, font=("Segoe UI", 12))
        entry.pack(fill="x", pady=10, ipady=8)
        results = tk.Frame(self.content, bg=BG)
        results.pack(fill="both", expand=True)
        def refresh(*_):
            for w in results.winfo_children():
                w.destroy()
            q = query.get().lower()
            matches = [s for s in self.songs if q in s["title"].lower() or q in s["artist"].lower()]
            self.song_list(matches, results)
        query.trace_add("write", refresh)
        refresh()
        entry.focus_set()

    def show_profile(self):
        messagebox.showinfo("InTune", "Profile and settings can be connected here.")

    def navigate(self, screen):
        if screen == "library":
            self.show_library()
        elif screen == "playlist":
            self.show_playlist()
        elif screen == "search":
            self.search_all()
        else:
            self.clear_content()
            self.heading("Home")
            tk.Label(self.content, text="Welcome to InTune", bg=BG, fg=MUTED,
                     font=("Segoe UI", 16)).pack(pady=35)

if __name__ == "__main__":
    root = tk.Tk()
    app = InTuneApp(root)
    root.mainloop()
