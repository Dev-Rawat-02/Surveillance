import subprocess
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk


BASE_DIR = Path(__file__).resolve().parent.parent
APP_PATH = BASE_DIR / "app.py"
DASHBOARD_PATH = BASE_DIR / "dashboard.py"


class SurveillanceLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Edge AI Surveillance")
        self.root.geometry("760x460")
        self.root.minsize(720, 420)
        self.root.configure(bg="#0b1220")

        self._build_styles()
        self._build_layout()

    def _build_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Root.TFrame", background="#0b1220")
        style.configure("Hero.TLabel", background="#0b1220", foreground="#f8fafc", font=("Segoe UI", 24, "bold"))
        style.configure("Body.TLabel", background="#0b1220", foreground="#94a3b8", font=("Segoe UI", 10))
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=(16, 10))
        style.map("Action.TButton", foreground=[("active", "#f8fafc")])

    def _build_layout(self):
        wrapper = ttk.Frame(self.root, style="Root.TFrame", padding=28)
        wrapper.pack(fill="both", expand=True)

        header = ttk.Frame(wrapper, style="Root.TFrame")
        header.pack(fill="x")

        ttk.Label(header, text="Edge AI Surveillance", style="Hero.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Simple control panel for the live detector, event dashboard, and snapshot history.",
            style="Body.TLabel",
        ).pack(anchor="w", pady=(8, 0))

        info = ttk.Frame(wrapper, style="Root.TFrame")
        info.pack(fill="x", pady=(28, 18))

        self._feature_card(info, "Live View", "Start the OpenCV surveillance window.")
        self._feature_card(info, "Dashboard", "Browse alerts and open saved snapshots.")
        self._feature_card(info, "Local Storage", "Events are stored in SQLite on disk.")

        actions = ttk.Frame(wrapper, style="Root.TFrame")
        actions.pack(fill="x", pady=(10, 0))

        ttk.Button(actions, text="Start Live Surveillance", style="Action.TButton", command=self.start_surveillance).pack(
            fill="x", pady=(0, 10)
        )
        ttk.Button(actions, text="Open Event Dashboard", style="Action.TButton", command=self.open_dashboard).pack(
            fill="x", pady=(0, 10)
        )
        ttk.Button(actions, text="Exit", style="Action.TButton", command=self.root.destroy).pack(fill="x")

    def _feature_card(self, parent, title, description):
        card = ttk.Frame(parent, style="Root.TFrame")
        card.pack(fill="x", pady=(0, 10))

        panel = tk.Frame(card, bg="#111827", bd=0, highlightthickness=1, highlightbackground="#1f2937")
        panel.pack(fill="x")

        tk.Label(panel, text=title, bg="#111827", fg="#f8fafc", font=("Segoe UI", 11, "bold"), anchor="w").pack(
            fill="x", padx=14, pady=(12, 2)
        )
        tk.Label(
            panel,
            text=description,
            bg="#111827",
            fg="#94a3b8",
            font=("Segoe UI", 9),
            anchor="w",
        ).pack(fill="x", padx=14, pady=(0, 12))

    def start_surveillance(self):
        subprocess.Popen([sys.executable, str(APP_PATH), "--run"], cwd=str(BASE_DIR))

    def open_dashboard(self):
        subprocess.Popen([sys.executable, str(DASHBOARD_PATH)], cwd=str(BASE_DIR))

    def run(self):
        self.root.mainloop()


def launch_ui():
    SurveillanceLauncher().run()