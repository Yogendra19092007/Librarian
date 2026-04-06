# main.py
# Entry point — role selector
# CO1: conditionals, basic Python program structure
# CO2: string usage in UI labels

import tkinter as tk
from tkinter import font

# ── Window setup ─────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Library Management System")
root.geometry("520x400")
root.resizable(False, False)
root.configure(bg="#0f172a")

# ── Fonts ─────────────────────────────────────────────────────────────────────
title_font  = font.Font(family="Segoe UI", size=24, weight="bold")
button_font = font.Font(family="Segoe UI", size=12, weight="bold")
sub_font    = font.Font(family="Segoe UI", size=11)
badge_font  = font.Font(family="Segoe UI", size=9)

# ── Header ────────────────────────────────────────────────────────────────────
tk.Label(root, text="Library Management System",
         fg="#f8fafc", bg="#0f172a", font=title_font).pack(pady=(30, 6))

tk.Label(root, text="Choose your role to continue",
         fg="#cbd5e1", bg="#0f172a", font=sub_font).pack(pady=(0, 6))

# CO2: string variable used in the label
co_note: str = "CO1 · CO2 · CO3 aligned project"
tk.Label(root, text=co_note, fg="#475569", bg="#0f172a",
         font=badge_font).pack(pady=(0, 28))

# ── Role buttons ──────────────────────────────────────────────────────────────
button_frame = tk.Frame(root, bg="#0f172a")
button_frame.pack(pady=10)

btn_style = {
    "bg": "#10b981", "fg": "#ffffff",
    "activebackground": "#059669", "activeforeground": "#ffffff",
    "bd": 0, "relief": "flat",
    "font": button_font, "width": 18, "height": 2, "cursor": "hand2",
}


def open_user() -> None:
    """CO1: conditional flow — destroy root before importing next module."""
    root.destroy()
    import user_login   # lazy import keeps startup fast


def open_librarian() -> None:
    root.destroy()
    import librarian


user_btn      = tk.Button(button_frame, text="👤  User Login",
                          command=open_user, **btn_style)
librarian_btn = tk.Button(button_frame, text="📚  Librarian Login",
                          command=open_librarian, **btn_style)

user_btn.grid(row=0, column=0, padx=15, pady=10)
librarian_btn.grid(row=0, column=1, padx=15, pady=10)

# ── Feature badges ────────────────────────────────────────────────────────────
features_frame = tk.Frame(root, bg="#1e293b", bd=0)
features_frame.pack(padx=40, pady=20, fill="x")

# CO2: list of strings iterated to build labels
features: list = [
    "CO1 — Datatypes & Conditionals",
    "CO2 — Strings & Data Structures",
    "CO3 — File & Exception Handling",
]
for feat in features:
    tk.Label(features_frame, text=f"  ✔  {feat}",
             fg="#94a3b8", bg="#1e293b",
             font=badge_font, anchor="w").pack(fill="x", padx=10, pady=3)

# ── Footer ────────────────────────────────────────────────────────────────────
tk.Label(root, text="Built with Python · Tkinter · SQLite",
         fg="#334155", bg="#0f172a", font=badge_font).pack(side="bottom", pady=14)

root.mainloop()