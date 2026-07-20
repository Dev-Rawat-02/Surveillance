import os
import tkinter as tk
from tkinter import ttk, messagebox

from core.database import DatabaseManager


class AlertDashboard:
    def __init__(self):
        self.database = DatabaseManager()
        self.root = tk.Tk()
        self.root.title("Surveillance Event Dashboard")
        self.root.geometry("980x620")
        self.root.minsize(900, 560)
        self.root.configure(bg="#0f172a")

        self._build_styles()
        self._build_layout()
        self.refresh()

    def _build_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dashboard.TFrame", background="#0f172a")
        style.configure("Header.TLabel", background="#0f172a", foreground="#f8fafc", font=("Segoe UI", 22, "bold"))
        style.configure("Subheader.TLabel", background="#0f172a", foreground="#94a3b8", font=("Segoe UI", 10))
        style.configure("StatCard.TFrame", background="#111827")
        style.configure("StatTitle.TLabel", background="#111827", foreground="#94a3b8", font=("Segoe UI", 9, "bold"))
        style.configure("StatValue.TLabel", background="#111827", foreground="#f8fafc", font=("Segoe UI", 18, "bold"))
        style.configure("Dashboard.Treeview", rowheight=28, font=("Segoe UI", 10))
        style.configure("Dashboard.Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _build_layout(self):
        container = ttk.Frame(self.root, style="Dashboard.TFrame", padding=20)
        container.pack(fill="both", expand=True)

        header = ttk.Frame(container, style="Dashboard.TFrame")
        header.pack(fill="x")

        ttk.Label(header, text="Event Dashboard", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Recent alerts from the local SQLite event log.",
            style="Subheader.TLabel",
        ).pack(anchor="w", pady=(4, 16))

        stats = ttk.Frame(container, style="Dashboard.TFrame")
        stats.pack(fill="x", pady=(0, 14))

        self.total_value = self._stat_card(stats, "Total Alerts", "0")
        self.latest_value = self._stat_card(stats, "Latest Event", "-")
        self.latest_label_value = self._stat_card(stats, "Latest Label", "-")

        toolbar = ttk.Frame(container, style="Dashboard.TFrame")
        toolbar.pack(fill="x", pady=(0, 10))

        ttk.Button(toolbar, text="Refresh", command=self.refresh).pack(side="left")
        ttk.Button(toolbar, text="Open Snapshot", command=self.open_snapshot).pack(side="left", padx=(8, 0))
        ttk.Label(
            toolbar,
            text="Double-click a row to open its snapshot.",
            style="Subheader.TLabel",
        ).pack(side="right")

        table_frame = ttk.Frame(container, style="Dashboard.TFrame")
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "timestamp", "label", "confidence", "snapshot")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Dashboard.Treeview")
        self.tree.heading("id", text="ID")
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.heading("label", text="Label")
        self.tree.heading("confidence", text="Confidence")
        self.tree.heading("snapshot", text="Snapshot Path")

        self.tree.column("id", width=70, anchor="center")
        self.tree.column("timestamp", width=180, anchor="w")
        self.tree.column("label", width=150, anchor="w")
        self.tree.column("confidence", width=110, anchor="center")
        self.tree.column("snapshot", width=420, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda event: self.open_snapshot())

    def _stat_card(self, parent, title, initial_value):
        card = ttk.Frame(parent, style="StatCard.TFrame", padding=16)
        card.pack(side="left", fill="x", expand=True, padx=(0, 12))

        ttk.Label(card, text=title, style="StatTitle.TLabel").pack(anchor="w")
        label = ttk.Label(card, text=initial_value, style="StatValue.TLabel")
        label.pack(anchor="w", pady=(6, 0))
        return label

    def refresh(self):
        alerts = self.database.fetch_alerts(limit=200)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for alert in alerts:
            self.tree.insert(
                "",
                "end",
                values=(
                    alert["id"],
                    alert["timestamp"],
                    alert["label"],
                    alert["confidence"],
                    alert["snapshot"],
                ),
            )

        self.total_value.config(text=str(self.database.count_alerts()))

        if alerts:
            latest = alerts[0]
            self.latest_value.config(text=latest["timestamp"])
            self.latest_label_value.config(text=latest["label"])
        else:
            self.latest_value.config(text="-")
            self.latest_label_value.config(text="-")

    def open_snapshot(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Open Snapshot", "Select an alert first.")
            return

        snapshot_path = self.tree.item(selection[0], "values")[4]
        if not snapshot_path:
            messagebox.showwarning("Open Snapshot", "This alert does not have a snapshot path.")
            return

        if not os.path.exists(snapshot_path):
            messagebox.showwarning("Open Snapshot", f"Snapshot not found:\n{snapshot_path}")
            return

        os.startfile(snapshot_path)

    def run(self):
        self.root.mainloop()


def launch_dashboard():
    AlertDashboard().run()