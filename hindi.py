import keyboard
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

hindi_letter_map = {
    # Vowels and vowel signs
    "A": "अ",
    "aa": "आ",
    "Aa": "आ",
    "AA": "आ",
    "AE": "ऐ",
    "E": "ए",
    "EE": "ई",
    "I": "इ",
    "O": "ओ",
    "OO": "ऊ",
    "OI": "ऐ",
    "OU": "औ",
    "U": "उ",
    "UU": "ऊ",
    "a": "ा",
    "ai": "ै",
    "au": "ौ",
    "e": "े",
    "ee": "ी",
    "i": "ि",
    "o": "ो",
    "oo": "ू",
    "u": "ू",
    "oh": "ः",
    "ou": "औ",
    "ri": "ृ",
    "RI": "ृ",

    # Consonants
    "b": "ब",
    "B": "ब",
    "bh": "भ",
    "BH": "भ",
    "c": "च",
    "C": "च",
    "ch": "छ",
    "CH": "छ",
    "d": "द",
    "D": "ड",
    "dh": "ध",
    "DH": "ढ",
    "f": "फ",
    "F": "फ",
    "ph": "फ",
    "PH": "फ",
    "g": "ग",
    "G": "ग",
    "gh": "घ",
    "GH": "घ",
    "gy": "ज्ञ",
    "GY": "ज्ञ",
    "h": "ह",
    "H": "ह",
    "j": "ज",
    "J": "ज",
    "jh": "झ",
    "JH": "झ",
    "k": "क",
    "K": "क",
    "kh": "ख",
    "KH": "ख",
    "ks": "क्ष",
    "KS": "क्ष",
    "l": "ल",
    "L": "ल",
    "m": "म",
    "M": "म",
    "n": "न",
    "N": "न",
    "ny": "ञ",
    "NY": "ञ",
    "p": "प",
    "P": "प",
    "q": "ं",
    "r": "र",
    "R": "र",
    "s": "स",
    "S": "ष",
    "x": "श",
    "t": "त",
    "T": "ट",
    "th": "थ",
    "TH": "ठ",
    "tr": "त्र",
    "TR": "त्र",
    "v": "व",
    "V": "व",
    "y": "य",
    "Y": "य",
    "z": "्",
    "Z": "्",

    # Special combinations
    "ng": "ं",
    "NG": "ं",

    # Numbers
    "0": "०",
    "1": "१",
    "2": "२",
    "3": "३",
    "4": "४",
    "5": "५",
    "6": "६",
    "7": "७",
    "8": "८",
    "9": "९",
}

ctrl = False
alt = False
last = ''
hindi_mode = False

def key_press(key):
    ch = key.name
    global ctrl, alt, last

    if ch == 'esc':  # Exit application
        close_app()
        return

    if ctrl:  # Handle Ctrl key combinations
        keyboard.press('ctrl+' + ch)
        return
    
    if ch == 'alt':  # Handle Alt key press
        alt = True
        return
    
    if not hindi_mode:  # Default English typing mode
        keyboard.press(key.name)
        return
    
    if alt:  # Handle Alt-specific mappings
        if (last + ch) in hindi_letter_map:
            keyboard.press('backspace')
            keyboard.press('backspace')
            keyboard.write(hindi_letter_map[last + ch])
            keyboard.write(hindi_letter_map['z'])
            last = ch
            return
        if ch in hindi_letter_map:
            keyboard.write(hindi_letter_map[ch])
            keyboard.write(hindi_letter_map['z'])
            last = ch
            return

    if (last + ch) in hindi_letter_map:  # Combine last and current key
        keyboard.press('backspace')
        keyboard.write(hindi_letter_map[last + ch])
        last = ch
        return

    last = ch  # Update the last key pressed

    if ch == 'ctrl':  # Track Ctrl key press
        ctrl = True

    if ch in hindi_letter_map.keys():  # Write mapped Hindi characters
        keyboard.write(hindi_letter_map[ch])
    else:  # Press unmapped characters as is
        keyboard.press(ch)
    return

def key_release(key):
    ch = key.name
    global ctrl, alt

    if ch in hindi_letter_map.keys():  # Skip releasing mapped keys
        return

    keyboard.release(ch)  # Release regular keys
    if ch == 'ctrl':  # Reset Ctrl flag
        ctrl = False
    if ch == 'alt':  # Reset Alt flag and press backspace
        alt = False
        keyboard.press('backspace')
    return

def toggle():  # Toggle between English and Hindi modes
    global hindi_mode
    hindi_mode = not hindi_mode
    toggle_button.config(text="Switch to English" if hindi_mode else "Switch to हिंदी")
    print(f"Mode: {'हिंदी' if hindi_mode else 'English'}")

def close_app():  # Clean up on application exit
    keyboard.unhook_all()
    root.destroy()

keyboard.on_press(key_press, suppress=True)  # Start key press listener
keyboard.on_release(key_release, suppress=True)  # Start key release listener

root = tk.Tk()
root.title("Keyboard Mapper")
root.geometry("400x250")
root.configure(bg='#333333')

font_style = tkFont.Font(family="Arial", size=14, weight="bold")

canvas = tk.Canvas(root, width=400, height=250)
canvas.place(x=0, y=0)
canvas.create_rectangle(0, 0, 400, 250, fill="#1f1f1f", outline="")

label = tk.Label(root, text="Keyboard Mapper Running . . .", fg="white", bg="#333333", font=font_style)
label.pack(padx=20, pady=30)

toggle_button = ttk.Button(
    root, 
    text="Switch to हिंदी", 
    command=toggle, 
    style="TButton",
)
toggle_button.pack(pady=30)

style = ttk.Style()
style.configure("TButton",
                font=('Arial', 12, 'bold'),
                padding=10,
                relief="flat",
                background="#444444",
                foreground="black")
style.map("TButton", background=[('active', '#555555')])

root.protocol("WM_DELETE_WINDOW", close_app)
root.mainloop()
