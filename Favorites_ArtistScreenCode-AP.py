
"""InTune UI Prototype: Favorites and Artist Info Screens."""
import tkinter as tk
from tkinter import ttk
import webbrowser
from urllib.parse import quote

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

# Theme Colors based on demo.py / song_detector.py
BG = "#11131b"
CARD = "#1e2230"
TEXT = "#f4f5fb"
MUTED = "#aeb5c7"
ACCENT = "#b6a0ff"
HEART_RED = "#fa647d"


class InTuneApp:
    def __init__(self, root):
        self.root = root
        self.setup_window(root, "InTune | Favorites Screen")
        root.protocol("WM_DELETE_WINDOW", root.destroy)

        self.images_ref = []
        
        # Header Section
        top_frame = tk.Frame(root, bg=BG)
        top_frame.pack(fill="x", padx=25, pady=(20, 10))
        self.label(top_frame, "00:00", 11, MUTED).pack(side="left")
        self.label(top_frame, "👤", 16, TEXT).pack(side="right")

        self.label(root, "Favorites", 26, TEXT).pack(anchor="w", padx=25, pady=(0, 15))

        # Search Bar
        search_frame = tk.Frame(root, bg=CARD, padx=12, pady=8)
        search_frame.pack(fill="x", padx=25, pady=(0, 15))
        self.label(search_frame, "🔍", 12, MUTED, CARD).pack(side="left", padx=(0, 8))
        self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 11), bg=CARD, fg=TEXT, insertbackground=TEXT, bd=0, highlightthickness=0)
        self.search_entry.insert(0, "Search")
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.label(search_frame, "✕", 11, MUTED, CARD).pack(side="right")

        # Track List Container
        tracks_frame = tk.Frame(root, bg=BG)
        tracks_frame.pack(fill="both", expand=True, padx=25)

        tracks_data = [
            ("Thinking Bout You", "Frank Ocean", "frank.jpg"),
            ("Beetlejuice", "Mariah the Scientist", "mariah.jpeg"),
            ("Blinding Lights", "The Weekend", "weekend.jpeg"),
            ("Fortworth", "Drake", "drake.jpeg"),
            ("Angels Smile", "NoCap", "nocap.jpeg")
        ]

        for title, artist, img_file in tracks_data:
            row = tk.Frame(tracks_frame, bg=BG, pady=6)
            row.pack(fill="x")

            photo = self.load_image(img_file, (45, 45))
            if photo:
                self.images_ref.append(photo)
                img_lbl = tk.Label(row, image=photo, bg=BG, bd=0)
                img_lbl.pack(side="left", padx=(0, 12))
            else:
                # Simulated Album Art Box
                art_fallback = tk.Canvas(row, width=42, height=42, bg=CARD, highlightthickness=0)
                art_fallback.pack(side="left", padx=(0, 12))
                art_fallback.create_rectangle(0, 0, 45, 45, fill="#353047", outline="")
                art_fallback.create_text(22, 22, text="🎵", fill=TEXT, font=("Segoe UI", 12))

            # Track Info
            info = tk.Frame(row, bg=BG)
            info.pack(side="left", fill="x", expand=True)
            self.label(info, title, 12, TEXT).pack(anchor="w")
            self.label(info, artist, 10, MUTED).pack(anchor="w")

            # Actions (Heart & Options)
            actions = tk.Frame(row, bg=BG)
            actions.pack(side="right")
            self.label(actions, "♥", 14, HEART_RED).pack(side="left", padx=10)
            
            # Clickable option dots that navigate to Artist Info Screen #6
            dots_btn = self.button(actions, "•••", lambda t=title: self.open_artist_screen(t), BG, MUTED)
            dots_btn.config(padx=2, pady=2, font=("Segoe UI", 10, "bold"))
            dots_btn.pack(side="left")

        # Bottom Player Controls Preview
        player_bar = tk.Frame(root, bg=CARD, padx=15, pady=12)
        player_bar.pack(fill="x", side="bottom")
        controls_text = "🔀      ⏮      ▶      ⏭      🔁"
        self.label(player_bar, controls_text, 12, TEXT, CARD).pack()

    @staticmethod
    def setup_window(window, title):
        window.title(title)
        window.geometry("420x720+100+50")
        window.resizable(False, False)
        window.configure(bg=BG)

    @staticmethod
    def label(parent, text, size=12, color=TEXT, bg=BG):
        return tk.Label(parent, text=text, font=("Segoe UI", size),
                        fg=color, bg=bg, wraplength=350)

    @staticmethod
    def button(parent, text, command, bg=CARD, fg=TEXT):
        return tk.Button(parent, text=text, command=command, font=("Segoe UI", 11, "bold"),
                         bg=bg, fg=fg, activebackground=bg, activeforeground=fg,
                         relief="flat", bd=0, padx=10, pady=6, cursor="hand2")

    def load_image(self, path, size):
        """Safely load and resize an image for Tkinter when Pillow is available."""
        if Image is None or ImageTk is None:
            return None
        try:
            with Image.open(path) as img:
                resampling = getattr(Image, "Resampling", Image)
                resized = img.resize(size, resampling.LANCZOS)
            return ImageTk.PhotoImage(resized)
        except Exception:
            return None

    def open_artist_screen(self, track_title):
        # Open Screen #6 (Artist Info Window)
        artist_win = tk.Toplevel(self.root)
        self.setup_window(artist_win, f"InTune | Artist Info Screen - {track_title}")

        back_btn = self.button(artist_win, "← Back to Favorites", lambda: artist_win.destroy(), CARD, TEXT)
        back_btn.pack(anchor="w", padx=25, pady=(15, 0))
        
        # Top Status / Profile
        top_frame = tk.Frame(artist_win, bg=BG)
        top_frame.pack(fill="x", padx=25, pady=(20, 10))
        self.label(top_frame, "00:00", 11, MUTED).pack(side="left")
        self.label(top_frame, "👤", 16, TEXT).pack(side="right")


        #self.label(artist_win, "The Weeknd", 22, TEXT).pack(anchor="w", padx=25, pady=(5, 2))
        #self.label(artist_win, "Abel Tesfaye | R&B / Pop", 11, MUTED).pack(anchor="w", padx=25, pady=(0, 15))

        # Search Bar
        search_frame = tk.Frame(artist_win, bg=CARD, padx=12, pady=8)
        search_frame.pack(fill="x", padx=25, pady=(0, 15))
        self.label(search_frame, "🔍", 12, MUTED, CARD).pack(side="left", padx=(0, 8))
        self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 11), bg=CARD, fg=TEXT, insertbackground=TEXT, bd=0, highlightthickness=0)
        self.search_entry.insert(0, "Search")
        self.search_entry.pack(side="left", fill="x", expand=True)

        # Artist Header Image
        banner_photo = self.load_image("theweekend.jpeg", (370, 140))
        if banner_photo:
            self.images_ref.append(banner_photo)
            banner_lbl = tk.Label(artist_win, image=banner_photo, bg=BG, bd=0)
            banner_lbl.pack(padx=25, pady=(0,10))
        else:
            art_canvas = tk.Canvas(artist_win, width=370, height=140, bg=CARD, highlightthickness=0)
            art_canvas.pack(padx=25, pady=(0, 10))
            art_canvas.create_rectangle(10, 10, 360, 130, fill="#353047", outline=ACCENT, width=1)
            art_canvas.create_text(185,70, text="[ The Weekend]\n(Add theweekend.jpg to folder)", fill=MUTED, font=("Segoe UI", 10), justify="center")

        # Artist Header Image placeholder
        #art_canvas = tk.Canvas(artist_win, width=370, height=140, bg=CARD, highlightthickness=0)
        #art_canvas.pack(padx=25, pady=(0, 10))
        #art_canvas.create_rectangle(10, 10, 360, 130, fill="#353047", outline=ACCENT, width=1)
        #art_canvas.create_text(185, 70, text="[ The Weeknd Artist Photo ]", fill=MUTED, font=("Segoe UI", 11))

        self.label(artist_win, "The Weeknd", 22, TEXT).pack(anchor="w", padx=25, pady=(5, 2))
        self.label(artist_win, "Abel Tesfaye | R&B / Pop", 11, MUTED).pack(anchor="w", padx=25, pady=(0, 15))

        # Action Buttons Row
        btn_row = tk.Frame(artist_win, bg=BG)
        btn_row.pack(fill="x", padx=25, pady=(0, 15))
        
        play_btn = self.button(btn_row, "▶  Play Music", lambda: webbrowser.open("https://open.spotify.com/search/The%20Weeknd"), CARD, TEXT)
        play_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        follow_btn = self.button(btn_row, "♡  Follow Artist", lambda: None, CARD, TEXT)
        follow_btn.pack(side="right", fill="x", expand=True, padx=(8, 0))

        # Related Songs Section
        self.label(artist_win, "Related Songs", 14, TEXT).pack(anchor="w", padx=25, pady=(5, 10))
        
        related_songs = [
            ("Starboy", "Starboy", "theweekend2.jpeg"),
            ("The Hills", "Beauty Behind the Madness", "theweekend3.jpeg")
        ]
        self.related_images = []
        for s_title, s_album, s_img in related_songs:
            s_row = tk.Frame(artist_win, bg=BG, pady=4)
            s_row.pack(fill="x", padx=25)

            rel_photo = self.load_image(s_img, (38, 38))
            if rel_photo:
                self.related_images.append(rel_photo)
                self.images_ref.append(rel_photo)
                rel_lbl = tk.Label(s_row, image=rel_photo, bg=BG)
                rel_lbl.pack(side="left", padx=(0, 10))
            else:
                thumb = tk.Canvas(s_row, width=36, height=36, bg=CARD, highlightthickness=0)
                thumb.pack(side="left", padx=(0, 10))
                thumb.create_rectangle(0, 0, 38, 38, fill="#353047")

            s_info = tk.Frame(s_row, bg=BG)
            s_info.pack(side="left", fill="x", expand=True)
            self.label(s_info, s_title, 11, TEXT).pack(anchor="w")
            self.label(s_info, s_album, 9, MUTED).pack(anchor="w")

            play_icon = self.button(s_row, "▶", lambda: None, CARD, TEXT)
            play_icon.config(padx=8, pady=2)
            play_icon.pack(side="right")

        # About Section
        self.label(artist_win, "About the Artist", 12, TEXT).pack(anchor="w", padx=25, pady=(15, 4))
        bio_text = "The Weeknd is a Canadian singer, songwriter, and record producer known for blending R&B with pop and electronic sounds."
        self.label(artist_win, bio_text, 9, MUTED).pack(anchor="w", padx=25)


if __name__ == "__main__":
    main_window = tk.Tk()
    app = InTuneApp(main_window)
    main_window.mainloop()
