import tkinter as tk
from tkinter import messagebox, filedialog
import random
import pyperclip


def encrypt(message, key):
    result = ""
    for char in message:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + key) % 26 + base
            result += chr(shifted)
        elif char.isdigit():
            shifted = (ord(char) - ord('0') + key) % 10 + ord('0')
            result += chr(shifted)
        else:
            result += char
    return result


def decrypt(message, key):
    return encrypt(message, -key)


def brute_force_decrypt(message):
    results = []
    for k in range(1, 26):
        results.append(f"Key {k}: {decrypt(message, k)}")
    return "\n".join(results)


# --- GUI Functions ---
def do_encrypt():
    text = input_text.get("1.0", tk.END).strip()
    key_input = key_entry.get().strip()
    if not text:
        messagebox.showwarning("Warning", "Enter a message first!")
        return

    if key_input == "":
        key = random.randint(1, 25)
        messagebox.showinfo("Random Key", f"🎲 Random key chosen: {key}")
    else:
        try:
            key = int(key_input)
            if not 1 <= key <= 25:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Key must be a number between 1 and 25")
            return

    encrypted = encrypt(text, key)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, encrypted)
    pyperclip.copy(encrypted)
    messagebox.showinfo("Copied", "Encrypted message copied to clipboard!")


def do_decrypt():
    text = input_text.get("1.0", tk.END).strip()
    key_input = key_entry.get().strip()
    if not text:
        messagebox.showwarning("Warning", "Enter a message first!")
        return

    try:
        key = int(key_input)
        if not 1 <= key <= 25:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Key must be a number between 1 and 25")
        return

    decrypted = decrypt(text, key)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, decrypted)
    pyperclip.copy(decrypted)
    messagebox.showinfo("Copied", "Decrypted message copied to clipboard!")


def do_bruteforce():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Enter an encrypted message first!")
        return
    results = brute_force_decrypt(text)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, results)


def save_file():
    content = output_text.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("Warning", "Nothing to save!")
        return
    file = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text Files", "*.txt")])
    if file:
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Saved", f"File saved as {file}")


def load_file():
    file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, content)


# --- Dark Mode Toggle ---
is_dark = False


def toggle_theme():
    global is_dark
    is_dark = not is_dark

    if is_dark:
        bg, fg = "#2E2E2E", "#FFFFFF"
    else:
        bg, fg = "#f4f4f9", "#000000"

    root.config(bg=bg)
    frame_top.config(bg=bg)
    frame_buttons.config(bg=bg)
    frame_bottom.config(bg=bg)

    for widget in frame_top.winfo_children() + frame_buttons.winfo_children() + frame_bottom.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=bg, fg=fg)
        elif isinstance(widget, tk.Text):
            widget.config(bg="#1E1E1E" if is_dark else "white",
                          fg=fg, insertbackground=fg)
        elif isinstance(widget, tk.Entry):
            widget.config(bg="#1E1E1E" if is_dark else "white",
                          fg=fg, insertbackground=fg)
        elif isinstance(widget, tk.Button):
            widget.config(fg=fg)


def fancy_button(master, text, command, bg, fg="white"):
    btn = tk.Button(master, text=text, command=command,
                    bg=bg, fg=fg, relief="flat", bd=0,
                    padx=12, pady=6, highlightthickness=0,
                    font=("Times New Roman", 14, "bold"), activebackground=bg)

    target_color = _lighten_color(bg, 0.3)
    normal_color = bg
    base_font = ("Times New Roman", 14, "bold")

    def on_enter(e):
        btn.config(bg=target_color, font=("Times New Roman", 16, "bold"))

    def on_leave(e):
        btn.config(bg=normal_color, font=base_font)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def add_focus_effect(widget):
    base_font = ("Times New Roman", 14)
    focus_font = ("Times New Roman", 16)

    def on_focus_in(e):
        widget.config(font=focus_font)

    def on_focus_out(e):
        widget.config(font=base_font)

    widget.bind("<FocusIn>", on_focus_in)
    widget.bind("<FocusOut>", on_focus_out)


def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def _lighten_color(color, factor=0.3):
    r, g, b = _hex_to_rgb(color)
    return _rgb_to_hex((min(255, int(r + (255 - r) * factor)),
                        min(255, int(g + (255 - g) * factor)),
                        min(255, int(b + (255 - b) * factor))))


# --- GUI Setup ---
root = tk.Tk()
root.title("🔒 CipherVault – Secret Messaging Tool")
root.geometry("717x717+0+0")
root.config(bg="#f4f4f9")

# Input Frame
frame_top = tk.Frame(root, bg="#f4f4f9")
frame_top.pack(pady=10, fill="x")

tk.Label(frame_top, text="Enter Message :--", bg="#f4f4f9",
         font=("Times New Roman", 14, "bold")).grid(row=0, column=0, sticky="w")

input_text = tk.Text(frame_top, width=90, height=5, wrap="word",
                     font=("Times New Roman", 14))
input_text.grid(row=1, column=0, padx=10, pady=5, columnspan=3)
add_focus_effect(input_text)

tk.Label(frame_top, text="Key (1 - 25) :--", bg="#f4f4f9",
         font=("Times New Roman", 14)).grid(row=2, column=0, sticky="w", pady=5)

key_entry = tk.Entry(frame_top, width=10, font=("Times New Roman", 14))
key_entry.grid(row=2, column=1, sticky="w")
add_focus_effect(key_entry)

# Buttons
frame_buttons = tk.Frame(root, bg="#f4f4f9")
frame_buttons.pack(pady=10)

fancy_button(frame_buttons, "Encrypt", do_encrypt,
             bg="#4CAF50").grid(row=0, column=0, padx=10)
fancy_button(frame_buttons, "Decrypt", do_decrypt,
             bg="#2196F3").grid(row=0, column=1, padx=10)
fancy_button(frame_buttons, "Brute Force", do_bruteforce,
             bg="#FF9800").grid(row=0, column=2, padx=10)
fancy_button(frame_buttons, "Save to File", save_file,
             bg="#9C27B0").grid(row=0, column=3, padx=10)
fancy_button(frame_buttons, "Load from File", load_file,
             bg="#795548").grid(row=0, column=4, padx=10)
fancy_button(frame_buttons, "🌙 Toggle Dark Mode", toggle_theme,
             bg="#607D8B").grid(row=1, column=0, columnspan=5, pady=10)

# Output Frame
frame_bottom = tk.Frame(root, bg="#f4f4f9")
frame_bottom.pack(pady=10, fill="both", expand=True, anchor="nw")

tk.Label(frame_bottom, text="Output :--", bg="#f4f4f9",
         font=("Times New Roman", 14, "bold")).pack(anchor="nw")

output_text = tk.Text(frame_bottom, width=90, height=12, wrap="word",
                      font=("Times New Roman", 14))
output_text.pack(padx=10, pady=5, anchor="nw")
add_focus_effect(output_text)

root.mainloop()
