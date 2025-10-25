import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD

# --- Main Window ---
root = TkinterDnD.Tk()
root.title("Molecule Viewer")

# ttk theme setup
style = ttk.Style(root)
style.theme_use("clam")
root.attributes("-fullscreen", True)


# (Optional) allow user to exit fullscreen with ESC
def exit_fullscreen(event=None):
    root.attributes("-fullscreen", False)


root.bind("<Escape>", exit_fullscreen)
root.minsize(850, 450)

# Custom ttk styling
style.configure("TFrame", background="#f4f6f8")
style.configure("TLabel", background="#f4f6f8", font=("Segoe UI", 10))
style.configure("TEntry", padding=6, font=("Segoe UI", 10))
style.configure("TButton", padding=6, font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 11, "bold"), foreground="#333")

root.config(bg="#f4f6f8")

# --- Top Frame (Search + Drag & Drop) ---
top_frame = ttk.Frame(root, padding=(15, 10))
top_frame.pack(fill="x")

# Search bar (left)
search_var = tk.StringVar()
search_entry = ttk.Entry(top_frame, textvariable=search_var, width=40)
search_entry.pack(side="left", padx=(0, 15))
search_entry.insert(0, "Search...")

# Drag & Drop Area (right)
drop_area = tk.Label(
    top_frame,
    text="📂 Drag & Drop Files Here",
    font=("Segoe UI", 10, "bold"),
    relief="ridge",
    borderwidth=2,
    width=30,
    height=3,
    bg="#ffffff",
    fg="#555555",
    highlightbackground="#c5c6c7",
    highlightthickness=1,
)
drop_area.pack(side="right", padx=(10, 5))


# Hover effects
def on_enter(e): drop_area.config(bg="#e9f2ff", fg="#2a63bf")


def on_leave(e): drop_area.config(bg="#ffffff", fg="#555555")


drop_area.bind("<Enter>", on_enter)
drop_area.bind("<Leave>", on_leave)

# --- Middle Frame (Files + Molecule Canvas) ---
bottom_frame = ttk.Frame(root, padding=15)
bottom_frame.pack(fill="both", expand=True)

# Left: Uploaded files
left_frame = ttk.Frame(bottom_frame)
left_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

list_label = ttk.Label(left_frame, text="Uploaded Files", style="Header.TLabel")
list_label.pack(anchor="w", pady=(0, 5))

listbox_frame = tk.Frame(left_frame, bg="#ffffff", bd=1, relief="solid")
listbox_frame.pack(fill="both", expand=True)

listbox = tk.Listbox(
    listbox_frame,
    height=15,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    bg="#ffffff",
    fg="#333",
    selectbackground="#d0e3ff",
    font=("Segoe UI", 10)
)
listbox.pack(fill="both", expand=True, padx=2, pady=2)

# Right: Molecule canvas
right_frame = ttk.Frame(bottom_frame)
right_frame.pack(side="right", fill="both", expand=True, padx=(8, 0))

canvas_label = ttk.Label(right_frame, text="Molecule Animation", style="Header.TLabel")
canvas_label.pack(anchor="w", pady=(0, 5))

canvas = tk.Canvas(right_frame, bg="#ffffff", highlightthickness=1, highlightbackground="#c5c6c7")
canvas.pack(fill="both", expand=True)

# --- Info Box (Bottom Console) ---
info_frame = ttk.Frame(root, padding=(15, 5))
info_frame.pack(fill="x")

info_label = ttk.Label(info_frame, text="Info / Log", style="Header.TLabel")
info_label.pack(anchor="w", pady=(0, 3))

info_box = tk.Text(
    info_frame,
    height=4,
    bg="#1e1e1e",
    fg="#e5e5e5",
    insertbackground="#ffffff",
    relief="flat",
    font=("Consolas", 10),
    wrap="word"
)
info_box.pack(fill="x", expand=False, padx=2, pady=2)
info_box.config(state="disabled")


def log_message(message: str):
    """Append a message to the info box."""
    info_box.config(state="normal")
    info_box.insert("end", f"• {message}\n")
    info_box.see("end")
    info_box.config(state="disabled")


# --- Handle file drop ---
def handle_drop(event):
    files = root.tk.splitlist(event.data)
    for f in files:
        filename = f.split("/")[-1]
        listbox.insert(tk.END, filename)
        log_message(f"Loaded file: {filename}")


drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind("<<Drop>>", handle_drop)


# --- Search filter ---
def filter_list(*args):
    text = search_var.get().lower()
    for i in range(listbox.size()):
        item = listbox.get(i)
        listbox.itemconfig(i, fg="black" if text in item.lower() else "#c0c0c0")


search_var.trace_add("write", filter_list)

# --- Run ---
log_message("Application started successfully.")
root.mainloop()
