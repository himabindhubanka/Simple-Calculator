import tkinter as tk
from tkinter import messagebox
import math

# ------------------- Themes -------------------
light_theme = {
    "bg": "#f4f4f4", "fg": "#000000", "entry_bg": "#ffffff", "entry_fg": "#000000",
    "button_bg": "#e6f7ff", "button_fg": "#000000", "active_bg": "#ccf2ff",
    "highlight": "#00bfff"
}

dark_theme = {
    "bg": "#121212", "fg": "#ffffff", "entry_bg": "#1e1e1e", "entry_fg": "#ffffff",
    "button_bg": "#2c2c2c", "button_fg": "#00ffcc", "active_bg": "#444444",
    "highlight": "#00ffcc"
}

current_theme = light_theme
scientific_mode = False
history_visible = True
history_list = []

# ------------------- Expression Evaluation -------------------
def evaluate_expression(expression):
    try:
        expression = expression.replace('^', '**').replace('%', '/100').replace('$', '')
        for func in ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp', 'pi', 'e']:
            if func in expression:
                expression = expression.replace(func, f'math.{func}')
        return str(eval(expression))
    except:
        return "Error"

# ------------------- History -------------------
def update_history(expr, result):
    if result != "Error":
        history_list.append(f"{expr} = {result}")
        if len(history_list) > 10:
            history_list.pop(0)
        show_history()

def show_history():
    history_label.config(state='normal')
    history_label.delete(1.0, tk.END)
    for item in history_list[::-1]:
        history_label.insert(tk.END, item + '\n')
    history_label.config(state='disabled')

def toggle_history():
    global history_visible
    history_visible = not history_visible
    if history_visible:
        history_label.pack(fill="x", padx=10, pady=5)
        show_history()
    else:
        history_label.pack_forget()

# ------------------- Theme Toggle -------------------
def toggle_theme():
    global current_theme
    current_theme = dark_theme if current_theme == light_theme else light_theme
    apply_theme()

# ------------------- Mode Toggle -------------------
def toggle_mode():
    global scientific_mode
    scientific_mode = not scientific_mode
    build_buttons()

# ------------------- Button Click -------------------
def click(event):
    btn_text = event.widget.cget("text")
    current = entry.get()
    if btn_text == "=":
        result = evaluate_expression(current)
        update_history(current, result)
        entry.delete(0, tk.END)
        entry.insert(0, result)
    elif btn_text == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, btn_text)

# ------------------- Keyboard Input -------------------
def key_press(event):
    key = event.char
    if key in "0123456789+-*/().%^":
        entry.insert(tk.END, key)
    elif key == "\r":
        result = evaluate_expression(entry.get())
        update_history(entry.get(), result)
        entry.delete(0, tk.END)
        entry.insert(0, result)
    elif key == "\x08":
        entry.delete(len(entry.get()) - 1, tk.END)

# ------------------- Settings Panel Toggle -------------------
def toggle_settings():
    if settings_frame.winfo_ismapped():
        settings_frame.pack_forget()
    else:
        settings_frame.pack(fill="x", padx=10, pady=(0, 10))

# ------------------- Apply Theme -------------------
def apply_theme():
    root.configure(bg=current_theme["bg"])
    entry.configure(bg=current_theme["entry_bg"], fg=current_theme["entry_fg"], insertbackground=current_theme["entry_fg"])
    for btn in buttons_refs:
        btn.configure(bg=current_theme["button_bg"], fg=current_theme["button_fg"], activebackground=current_theme["active_bg"])
    settings_button.configure(bg=current_theme["button_bg"], fg=current_theme["button_fg"], activebackground=current_theme["active_bg"])
    for widget in settings_frame.winfo_children():
        widget.configure(bg=current_theme["button_bg"], fg=current_theme["button_fg"])
    history_label.configure(bg=current_theme["entry_bg"], fg=current_theme["fg"], highlightbackground=current_theme["bg"])

# ------------------- Build Buttons -------------------
def build_buttons():
    for widget in button_area.winfo_children():
        widget.destroy()
    buttons_refs.clear()

    buttons = scientific_buttons if scientific_mode else standard_buttons
    for row in buttons:
        frame = tk.Frame(button_area, bg=current_theme["bg"])
        frame.pack(expand=True, fill="both")
        for text in row:
            if text == "":
                tk.Label(frame, text="", bg=current_theme["bg"]).pack(side="left", expand=True, fill="both")
            else:
                btn = tk.Button(frame, text=text, font=("Arial", 16))
                btn.pack(side="left", expand=True, fill="both", padx=2, pady=2)
                btn.bind("<Button-1>", click)
                buttons_refs.append(btn)
    apply_theme()

# ------------------- Layout -------------------
root = tk.Tk()
root.title("Smart Calculator")
root.geometry("400x700")
root.resizable(False, False)

# Center the window
w, h = 400, 700
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws // 2) - (w // 2)
y = (hs // 2) - (h // 2)
root.geometry(f"{w}x{h}+{x}+{y}")

# Entry + Settings Button
top_frame = tk.Frame(root, bg=current_theme["bg"])
top_frame.pack(fill="x", pady=(10, 0))

entry = tk.Entry(top_frame, font="Arial 24", bd=5, relief=tk.FLAT, justify="right", width=15)
entry.pack(side="left", padx=(10, 5), pady=10, ipady=10, fill="x", expand=True)

settings_button = tk.Button(top_frame, text="⚙️", font=("Arial", 14), command=toggle_settings, width=4)
settings_button.pack(side="right", padx=(5, 10))

# Settings Frame inside calculator
settings_frame = tk.Frame(root, bg=current_theme["button_bg"])

tk.Button(settings_frame, text="Toggle Theme", font=("Arial", 12), command=toggle_theme).pack(fill="x", pady=2)
tk.Button(settings_frame, text="Switch Mode", font=("Arial", 12), command=toggle_mode).pack(fill="x", pady=2)
tk.Button(settings_frame, text="Toggle History", font=("Arial", 12), command=toggle_history).pack(fill="x", pady=2)

# History label
history_label = tk.Text(root, font=("Arial", 10), height=5, state='disabled', wrap="word", bd=1, relief=tk.SOLID)
history_label.pack(fill="x", padx=10, pady=5)

# Button Area
button_area = tk.Frame(root, bg=current_theme["bg"])
button_area.pack(expand=True, fill="both", padx=10)

# Layouts
standard_buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '%', '+'],
    ['C', '(', ')', '='],
    ['$', '^', 'log', '']
]

scientific_buttons = [
    ['sin', 'cos', 'tan', 'sqrt'],
    ['log', 'exp', 'pi', 'e'],
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '^', '+'],
    ['(', ')', 'C', '=']
]

buttons_refs = []

# Start UI
build_buttons()
apply_theme()
show_history()
root.bind("<Key>", key_press)
root.mainloop()

