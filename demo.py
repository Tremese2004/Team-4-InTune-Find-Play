"""Song Detector: a two-window UI demo, with simulated recognition only."""
import tkinter as tk
from tkinter import ttk
import webbrowser
from urllib.parse import quote

BG = "#11131b"
CARD = "#1e2230"
TEXT = "#f4f5fb"
MUTED = "#aeb5c7"
ACCENT = "#b6a0ff"


class SongDetector:
    def __init__(self, root):
        self.root = root
        self.result = None
        self.listening = False
        self.step = 0
        self.setup_window(root, "Song Detector | Detector")
        root.protocol("WM_DELETE_WINDOW", root.destroy)
        self.label(root, "SONG DETECTOR", 11, ACCENT).pack(pady=(30, 12))
        self.label(root, "What's that song?", 28).pack()
        self.label(root, "Find a song. Choose where to listen.", 11, MUTED).pack(pady=(8, 24))
        card = tk.Frame(root, bg=CARD, padx=25, pady=22)
        card.pack(fill="x", padx=35)
        self.label(card, "DEMO MODE", 10, ACCENT, CARD).pack()
        self.label(card, "No microphone or account needed", 13, bg=CARD).pack(pady=10)
        self.label(card, "Recognition is simulated for this presentation.", 10, MUTED, CARD).pack()
        self.bars = tk.Canvas(root, width=280, height=62, bg=BG, highlightthickness=0)
        self.bars.pack(pady=(22, 8))
        self.draw_bars()
        self.status = self.label(root, "Ready to try a demo detection", 11, MUTED)
        self.status.pack(pady=(0, 12))
        self.detect_button = self.button(root, "Detect demo song", self.detect, ACCENT, BG)
        self.detect_button.pack(fill="x", padx=70, pady=8)
        self.progress = ttk.Progressbar(root, mode="determinate", maximum=10)
        self.progress.pack(fill="x", padx=70, pady=(8, 18))
        self.label(root, "Spotify  /  Apple Music", 11, MUTED).pack()
        self.label(root, "Python desktop prototype", 9, MUTED).pack(pady=10)

    @staticmethod
    def setup_window(window, title):
        window.title(title)
        window.geometry("560x610+100+70")
        window.resizable(False, False)
        window.configure(bg=BG)

    @staticmethod
    def label(parent, text, size=12, color=TEXT, bg=BG):
        return tk.Label(parent, text=text, font=("Segoe UI", size),
                        fg=color, bg=bg, wraplength=465)

    @staticmethod
    def button(parent, text, command, bg=CARD, fg=TEXT):
        return tk.Button(parent, text=text, command=command, font=("Segoe UI", 12, "bold"),
                         bg=bg, fg=fg, activebackground=bg, activeforeground=fg,
                         relief="flat", bd=0, padx=16, pady=12, cursor="hand2",
                         disabledforeground="#555367")

    def draw_bars(self):
        self.bars.delete("all")
        for i in range(21):
            height = 8 + ((i * 13 + self.step * 9) % 43)
            self.bars.create_rectangle(8 + i * 13, 31 - height / 2,
                                       14 + i * 13, 31 + height / 2,
                                       fill=ACCENT if self.listening else "#454055", outline="")

    def detect(self):
        if self.listening:
            return
        self.listening = True
        self.step = 0
        self.detect_button.config(state="disabled", text="Listening...")
        self.status.config(text="Listening to the sample... (simulated)")
        self.tick()

    def tick(self):
        self.step += 1
        self.progress["value"] = self.step
        self.draw_bars()
        if self.step < 10:
            self.root.after(180, self.tick)
        else:
            self.listening = False
            self.detect_button.config(state="normal", text="Detect demo song")
            self.status.config(text="Demo song found. See the result window.")
            self.show_result()

    def show_result(self):
        self.result = tk.Toplevel(self.root)
        self.setup_window(self.result, "Song Detector | Song result")
        self.result.protocol("WM_DELETE_WINDOW", self.back)
        self.label(self.result, "SONG FOUND / DEMO RESULT", 11, ACCENT).pack(pady=(30, 22))
        art = tk.Canvas(self.result, width=150, height=150, bg=CARD, highlightthickness=0)
        art.pack()
        art.create_oval(22, 22, 128, 128, fill="#353047", outline=ACCENT, width=3)
        art.create_oval(52, 52, 98, 98, fill=BG, outline=ACCENT, width=2)
        art.create_oval(70, 70, 80, 80, fill=ACCENT, outline="")
        self.label(self.result, "Blinding Lights", 26).pack(pady=(18, 4))
        self.label(self.result, "The Weeknd", 14, MUTED).pack()
        self.label(self.result, "Sample result for the prototype", 10, MUTED).pack(pady=(10, 18))
        self.button(self.result, "Search on Spotify", lambda: self.open_service("spotify"),
                    "#1db954", BG).pack(fill="x", padx=70, pady=5)
        self.button(self.result, "Search on Apple Music", lambda: self.open_service("apple"),
                    "#fa647d", BG).pack(fill="x", padx=70, pady=5)
        self.button(self.result, "Back to detector", self.back).pack(fill="x", padx=70, pady=(16, 8))
        self.label(self.result, "Music buttons open searches in your browser.", 9, MUTED).pack()
        self.root.withdraw()
        self.result.lift()
        self.result.focus_set()

    def open_service(self, service):
        query = quote("Blinding Lights The Weeknd")
        url = ("https://open.spotify.com/search/" + query if service == "spotify"
               else "https://music.apple.com/us/search?term=" + query)
        webbrowser.open(url)

    def back(self):
        if self.result is not None:
            self.result.destroy()
            self.result = None
        self.root.deiconify()
        self.root.lift()
        self.progress["value"] = 0
        self.status.config(text="Ready to try another demo detection")
        self.draw_bars()


if __name__ == "__main__":
    main_window = tk.Tk()
    app = SongDetector(main_window)
    main_window.mainloop()
