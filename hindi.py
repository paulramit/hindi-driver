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
    "Ae": "ऐ",
    "E": "ए",
    "Ee": "ई",
    "I": "इ",
    "O": "ओ",
    "Oo": "ऊ",
    "OI": "ऐ",
    "Ou": "औ",
    "U": "उ",
    "Uu": "ऊ",
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
    "Ri": "ृ",

    # Consonants
    "b": "ब",
    "B": "ब",
    "bh": "भ",
    "Bh": "भ",
    "c": "च",
    "C": "च",
    "ch": "छ",
    "Ch": "छ",
    "d": "द",
    "D": "ड",
    "dh": "ध",
    "Dh": "ढ",
    "f": "फ",
    "F": "फ",
    "ph": "फ",
    "g": "ग",
    "G": "ग",
    "gh": "घ",
    "Gh": "घ",
    "gy": "ज्ञ",
    "Gy": "ज्ञ",
    "h": "ह",
    "H": "ह",
    "j": "ज",
    "J": "ज",
    "jh": "झ",
    "Jh": "झ",
    "k": "क",
    "K": "क",
    "kh": "ख",
    "Kh": "ख",
    "ksh": "क्ष",
    "l": "ल",
    "L": "ल",
    "m": "म",
    "M": "म",
    "n": "न",
    "N": "न",
    "ny": "ञ",
    "p": "प",
    "P": "प",
    "q": "ं",
    "r": "र",
    "R": "र",
    "s": "स",
    "S": "ष",
    "t": "त",
    "t'": "ट",
    "T": "ट",
    "th": "थ",
    "th'": "ठ",
    "Th": "ठ",
    "tr": "त्र",
    "Tr": "त्र",
    "v": "व",
    "V": "व",
    "y": "य",
    "Y": "य",
    "z": "्",

    # Special combinations
    "ng": "ं",

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
hindi_mode = False  # Track the current mode

# Function to handle key press events
def key_press(key):

    ch = key.name
    global ctrl
    global alt
    global last

    if ch == 'esc':  # Quit if ESC pressed
        close_app()
        return

    if ctrl:  # Check if Ctrl was pressed
        keyboard.press('ctrl+' + ch)
        return
    
    if ch == 'alt':
        alt = True
        return
    
    if not hindi_mode:
        keyboard.press(key.name)
        return  # Skip processing if in normal mode
    
    if alt:
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

    if (last + ch) in hindi_letter_map:
        keyboard.press('backspace')
        keyboard.write(hindi_letter_map[last + ch])
        last = ch
        return

    last = ch

    if ch == 'ctrl':
        ctrl = True

    if ch in hindi_letter_map.keys():
        keyboard.write(hindi_letter_map[ch])
    else:
        keyboard.press(ch)  # Press key if not in hindi_letter_map
    return

# Function to handle key release events
def key_release(key):

    ch = key.name
    global ctrl
    global alt
    if ch in hindi_letter_map.keys():  # Keys in hindi_letter_map were suppressed during press event; no need to release
        return

    keyboard.release(ch)  # Release key ch
    if ch == 'ctrl':  # Ctrl is released
        ctrl = False
    if ch == 'alt':  # Alt is released
        alt = False
        keyboard.press('backspace')
    return

# Function to toggle between English and Hindi modes
def toggle():
    global hindi_mode
    hindi_mode = not hindi_mode
    toggle_button.config(text="Switch to English" if hindi_mode else "Switch to हिंदी")
    print(f"Mode: {'हिंदी' if hindi_mode else 'English'}")

# Function to close app and unregister keyboard events
def close_app():
    keyboard.unhook_all()  # Disable all keyboard listeners
    root.destroy()  # Close the tkinter window

# Start keyboard listeners
keyboard.on_press(key_press, suppress=True)  # Call key_press on key press event
keyboard.on_release(key_release, suppress=True)  # Call key_release on key release event

# Create a small tkinter window
root = tk.Tk()
root.title("Keyboard Mapper")
root.geometry("400x250")  # Adjust window size for better layout
root.configure(bg='#333333')  # Dark background color

# Load custom font for a more modern look
font_style = tkFont.Font(family="Arial", size=14, weight="bold")

# Gradient Background (in case you want to create one using canvas)
canvas = tk.Canvas(root, width=400, height=250)
canvas.place(x=0, y=0)
canvas.create_rectangle(0, 0, 400, 250, fill="#1f1f1f", outline="")

# Label widget with custom font and color
label = tk.Label(root, text="Keyboard Mapper Running", fg="white", bg="#333333", font=font_style)
label.pack(padx=20, pady=30)  # Add the label to the window with padding

# Toggle button with modern flat design and rounded corners
toggle_button = ttk.Button(
    root, 
    text="Switch to हिंदी", 
    command=toggle, 
    style="TButton",
)
toggle_button.pack(pady=30)  # Add the button to the window with vertical padding

# Button Style (Rounded and Flat)
style = ttk.Style()
style.configure("TButton",
                font=('Arial', 12, 'bold'),
                padding=10,
                relief="flat",  # Flat button (no border)
                background="#444444",  # Dark gray button color
                foreground="black")  # Set text color to black
style.map("TButton", background=[('active', '#555555')])

# Close event handler
root.protocol("WM_DELETE_WINDOW", close_app)

# Start tkinter main loop
root.mainloop()  # Keep the tkinter window running