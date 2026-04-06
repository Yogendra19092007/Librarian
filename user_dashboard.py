import tkinter as tk
from tkinter import font
import backend

root = tk.Tk()
root.title("User Dashboard")
root.geometry("520x420")
root.resizable(False, False)
root.configure(bg="#090c15")

header_font = font.Font(family="Segoe UI", size=24, weight="bold")
label_font = font.Font(family="Segoe UI", size=12)
button_font = font.Font(family="Segoe UI", size=12, weight="bold")

header = tk.Label(root, text="Welcome to Your Dashboard", fg="#eef2ff", bg="#090c15", font=header_font)
header.pack(pady=(25, 10))

sub = tk.Label(root, text="Quick access to borrowing, returning and checking books", fg="#cbd5e1", bg="#090c15", font=label_font)
sub.pack(pady=(0, 20))

card = tk.Frame(root, bg="#111827", bd=0)
card.pack(padx=25, pady=10, fill='both', expand=True)

status_text = "Logged in as: " + (backend.current_user['lib_id'] if backend.current_user else "Guest")
status = tk.Label(card, text=status_text, fg="#f8fafc", bg="#111827", font=label_font)
status.pack(pady=(20, 10))

button_frame = tk.Frame(card, bg="#111827")
button_frame.pack(pady=10)

button_style = {'bg': '#7c3aed', 'fg': '#ffffff', 'activebackground': '#6d28d9', 'activeforeground': '#ffffff', 'bd': 0, 'font': button_font, 'width': 18, 'height': 2, 'cursor': 'hand2'}

def borrow():
    backend.open_borrow_dialog()


def return_book():
    backend.open_return_dialog()


def check():
    backend.open_check_dialog()


def show_history():
    backend.show_user_history()

borrow_btn = tk.Button(button_frame, text="Borrow Book", command=borrow, **button_style)
borrow_btn.grid(row=0, column=0, padx=10, pady=10)
return_btn = tk.Button(button_frame, text="Return Book", command=return_book, **button_style)
return_btn.grid(row=0, column=1, padx=10, pady=10)
check_btn = tk.Button(button_frame, text="Check Availability", command=check, **button_style)
check_btn.grid(row=1, column=0, padx=10, pady=10)
history_btn = tk.Button(button_frame, text="Borrow History", command=show_history, **button_style)
history_btn.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()