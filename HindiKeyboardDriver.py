import keyboard
from string import ascii_lowercase
from string import ascii_uppercase
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
5
# Global variables
eng2hind = {
    'a': 'अ',
    'b': 'ब',
    'bh': 'भ',
    'c': 'च',
    'ch': 'छ',
    'd': 'द',
    'dh': 'ध',
    'e': 'े',
    'ee': 'ी',
    'f': 'फ',
    'g': 'ग',
    'gh': 'घ',
    'h': 'ह',
    'oh': 'ः',
    'i': 'ि',
    'j': 'ज',
    'jh': 'झ',
    'k': 'क',
    'kh': 'ख',
    'l': 'ल',
    'm': 'म',
    'n': 'न',
    'o': 'ो',
    'ou': 'ौ',
    'oi': 'ै',
    'p': 'प',
    'ph': 'फ',
    'q': 'ं',
    'r': 'र',
    'Ri': 'ृ',
    's': 'स',
    't': 'त',
    'th': 'थ',
    'u': 'ु',
    'oo': 'ू',
    'w': 'ं',
    'x': 'श',
    'y': 'य',
    'z': '्',
    '[': '़',
    'A': 'आ',
    'B': 'ब',
    'C': '',
    'D': 'ड',
    'Dh': 'ढ',
    'E': 'ए',
    'EE': 'ई',
    'F': '',
    'G': '',
    'H': 'ह',
    'I': 'इ',
    'J': 'ज',
    'Jh': 'झ',
    'K': '',
    'L': '',
    'M': '',
    'N': 'ण',
    'O': 'ओ',
    'OU': 'औ',
    'OI': 'ऐ',
    'P': '',
    'Q': 'अ',
    'R': 'र',
    'RI': 'ऋ',
    'S': 'ष',
    'T': 'ट',
    'Th': 'ठ',
    'U': 'उ',
    'OO': 'ऊ',
    'V': '',
    'W': 'ञ',
    'X': '',
    'Y': '',
    'Z': '',
    'ng': 'ं',
    '1': '१',
    '2': '२',
    '3': '३',
    '4': '४',
    '5': '५',
    '6': '६',
    '7': '७',
    '8': '८',
    '9': '९',
    '0': '०'
}
ctrl = False
alt = False
last = ''
hindi_mode = False  # Track the current mode

# Function to handle key press events
def pressed1(name):
    

    ch = name.name
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
        keyboard.press(name.name)
        return  # Skip processing if in normal mode
    
    if (last == 'space' or last == '') and ch == 'o':
        keyboard.write(eng2hind['Q'])
        last = ch
        return
    
    if alt:
        if (last + ch) in eng2hind:
            keyboard.press('backspace')
            keyboard.press('backspace')
            keyboard.write(eng2hind[last + ch])
            keyboard.write(eng2hind['z'])
            last = ch
            return
        if ch in eng2hind:
            keyboard.write(eng2hind[ch])
            keyboard.write(eng2hind['z'])
            last = ch
            return

    if (last + ch) in eng2hind:
        keyboard.press('backspace')
        keyboard.write(eng2hind[last + ch])
        last = ch
        return


    if ch == 'Y':
        keyboard.write(eng2hind['z'])
        keyboard.write(eng2hind['y'])
        last = ch
        return

    last = ch

    if ch == 'ctrl':
        ctrl = True

    if ch in eng2hind.keys():
        keyboard.write(eng2hind[ch])
    else:
        keyboard.press(ch)  # Press key if not in eng2beng
    return

# Function to handle key release events
def released1(name):

    ch = name.name
    global ctrl
    global alt
    if ch in eng2hind.keys():  # Keys in eng2beng were suppressed during press event; no need to release
        return

    keyboard.release(ch)  # Release key ch
    if ch == 'ctrl':  # Ctrl is released
        ctrl = False
    if ch == 'alt':  # Alt is released
        alt = False
        keyboard.press('backspace')
    return

# Function to toggle between normal and Bengali modes
def toggle_mode():
    global hindi_mode
    hindi_mode = not hindi_mode
    toggle_button.config(text="Switch to English" if hindi_mode else "Switch to हिंदी")
    print(f"Mode: {'हिंदी' if hindi_mode else 'Normal'}")

# Function to close app and unregister keyboard events
def close_app():
    keyboard.unhook_all()  # Disable all keyboard listeners
    root.destroy()  # Close the tkinter window

# Load mappings from file
# f1 = open("./map.txt", "r", encoding="utf8")  # Open map.txt with utf8 encoding
# lines = f1.readlines()  # Read lines into array

# for line in lines:
#     a = line.split(":")[0]  # Split each line by ':', left - English char
#     b = line.split(":")[1].strip()  # Right - Bengali char, remove end '\n'
#     eng2beng[a] = b

# f1.close()

# Start keyboard listeners
keyboard.on_press(pressed1, suppress=True)  # Call pressed1 on key press event
keyboard.on_release(released1, suppress=True)  # Call released1 on key release event

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
    command=toggle_mode, 
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

