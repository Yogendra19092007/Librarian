import tkinter as tk
from tkinter import font, messagebox
import backend

root = tk.Tk()
root.title("User Login")
root.geometry("460x320")
root.resizable(False, False)
root.configure(bg="#111827")

header_font = font.Font(family="Segoe UI", size=22, weight="bold")
label_font = font.Font(family="Segoe UI", size=12)
entry_font = font.Font(family="Segoe UI", size=12)
button_font = font.Font(family="Segoe UI", size=12, weight="bold")

container = tk.Frame(root, bg="#1f2937", bd=0)
container.place(relx=0.5, rely=0.5, anchor='center', width=400, height=240)

header = tk.Label(container, text="Member Login", fg="#ffffff", bg="#1f2937", font=header_font)
header.pack(pady=(20, 10))

info = tk.Label(container, text="Enter your Library ID to continue", fg="#cbd5e1", bg="#1f2937", font=label_font)
info.pack(pady=(0, 20))

lib_id = tk.StringVar()
entry = tk.Entry(container, textvariable=lib_id, font=entry_font, bd=0, highlightthickness=2, highlightbackground="#334155", highlightcolor="#60a5fa", bg="#0f172a", fg="#f8fafc", insertbackground="#f8fafc")
entry.pack(ipady=8, padx=30, fill='x')

button = tk.Button(container, text="Login", command=lambda: login(), bg="#3b82f6", fg="#ffffff", activebackground="#2563eb", activeforeground="#ffffff", bd=0, font=button_font, cursor='hand2')
button.pack(pady=20, ipadx=10, ipady=6)


def login():
    if backend.validate_user(lib_id.get().strip()):
        root.destroy()
        import user_dashboard
    else:
        messagebox.showerror("Login Failed", "Invalid Library ID. Please try again.", parent=root)

root.mainloop()