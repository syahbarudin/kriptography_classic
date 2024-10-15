import tkinter as tk
from tkinter import messagebox

# Caesar Cipher encryption/decryption (shift 3)
def caesar_cipher(text, encrypt=True):
    shift = 3
    result = ""
    
    for char in text:
        if char.isupper():
            if encrypt:
                result += chr((ord(char) + shift - 65) % 26 + 65)
            else:
                result += chr((ord(char) - shift - 65) % 26 + 65)
        elif char.islower():
            if encrypt:
                result += chr((ord(char) + shift - 97) % 26 + 97)
            else:
                result += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            result += char
    
    return result

# Vigenère Cipher encryption/decryption
def vigenere_cipher(text, key, encrypt=True):
    key = key.lower()
    result = ""
    key_index = 0
    
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 97
            if char.isupper():
                base = 65
            else:
                base = 97
            
            if encrypt:
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += chr((ord(char) - base - shift) % 26 + base)
                
            key_index += 1
        else:
            result += char
    
    return result

# Atbash Cipher encryption/decryption (same for both)
def atbash_cipher(text):
    result = ""
    
    for char in text:
        if char.isupper():
            result += chr(90 - (ord(char) - 65))
        elif char.islower():
            result += chr(122 - (ord(char) - 97))
        else:
            result += char
    
    return result

# Playfair Cipher encryption/decryption (simplified version)
def playfair_cipher(text, key, encrypt=True):
    # Generate the 5x5 playfair matrix
    alphabet = "abcdefghiklmnopqrstuvwxyz"  # no 'j'
    matrix = [[None] * 5 for _ in range(5)]
    used = set()
    row, col = 0, 0
    
    # Fill the matrix with the key
    for char in key.lower():
        if char not in used and char != 'j':
            matrix[row][col] = char
            used.add(char)
            col += 1
            if col == 5:
                col = 0
                row += 1
    
    # Fill the rest of the matrix with remaining letters
    for char in alphabet:
        if char not in used:
            matrix[row][col] = char
            col += 1
            if col == 5:
                col = 0
                row += 1

    def find_position(letter):
        for r in range(5):
            for c in range(5):
                if matrix[r][c] == letter:
                    return r, c
        return None, None
    
    # Encrypt or decrypt the text
    result = ""
    text = text.lower().replace("j", "i")
    if len(text) % 2 != 0:
        text += 'x'
    
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        row1, col1 = find_position(a)
        row2, col2 = find_position(b)
        
        if row1 == row2:
            if encrypt:
                result += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            else:
                result += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            if encrypt:
                result += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                result += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
        else:
            result += matrix[row1][col2] + matrix[row2][col1]
    
    return result

# Function to reset all other checkboxes when one is selected
def on_cipher_select(selected_cipher):
    for cipher, var in cipher_vars.items():
        if cipher != selected_cipher:
            var.set(0)

# UI for choosing cipher and performing encryption/decryption
def handle_cipher(action):
    message = entry_text.get()
    key = entry_key.get() if cipher_vars['Vigenere'].get() or cipher_vars['Playfair'].get() else None
    
    if not message:
        messagebox.showwarning("Warning", "Please enter a message.")
        return
    
    if (cipher_vars['Vigenere'].get() or cipher_vars['Playfair'].get()) and not key:
        messagebox.showwarning("Warning", "Please enter a key.")
        return
    
    # Determine which cipher is selected
    if cipher_vars['Caesar'].get():
        result = caesar_cipher(message, encrypt=(action == 'Encrypt'))
    elif cipher_vars['Vigenere'].get():
        result = vigenere_cipher(message, key, encrypt=(action == 'Encrypt'))
    elif cipher_vars['Atbash'].get():
        result = atbash_cipher(message)
    elif cipher_vars['Playfair'].get():
        result = playfair_cipher(message, key, encrypt=(action == 'Encrypt'))
    else:
        messagebox.showwarning("Warning", "Please select a cipher.")
        return
    
    # Show the result in a messagebox with larger font
    result_window = tk.Toplevel()
    result_window.title(f"{action} Result")
    result_text = tk.Text(result_window, height=10, width=50, font=('Helvetica', 12))  # Bigger text size
    result_text.pack(pady=10)
    result_text.insert(tk.END, f"{action}ed Message: {result}")
    result_text.config(state=tk.DISABLED)

# Main window
root = tk.Tk()
root.title("Cipher Tool with Checkbox")
root.geometry("500x450")

# Label for cipher selection
cipher_label = tk.Label(root, text="Select Cipher:")
cipher_label.pack(pady=5)

# Variables for checkboxes
cipher_vars = {
    "Caesar": tk.IntVar(),
    "Vigenere": tk.IntVar(),
    "Atbash": tk.IntVar(),
    "Playfair": tk.IntVar(),
}

# Adding checkboxes for cipher selection
for cipher_name in cipher_vars.keys():
    checkbox = tk.Checkbutton(
        root, text=cipher_name, variable=cipher_vars[cipher_name], 
        command=lambda c=cipher_name: on_cipher_select(c)
    )
    checkbox.pack(pady=2)

# Input for the message (larger text area)
text_label = tk.Label(root, text="Enter your message:")
text_label.pack(pady=5)

entry_text = tk.Entry(root, width=50, font=('Helvetica', 12))  # Bigger textbox and font
entry_text.pack(pady=5)

# Input for the key (only for Vigenere and Playfair, larger text area)
key_label = tk.Label(root, text="Enter the key (if required):")
key_label.pack(pady=5)

entry_key = tk.Entry(root, width=50, font=('Helvetica', 12))  # Bigger textbox and font
entry_key.pack(pady=5)

# Encrypt button
encrypt_button = tk.Button(root, text="Encrypt", command=lambda: handle_cipher("Encrypt"), width=20)
encrypt_button.pack(pady=10)

# Decrypt button
decrypt_button = tk.Button(root, text="Decrypt", command=lambda: handle_cipher("Decrypt"), width=20)
decrypt_button.pack(pady=10)

# Run the application
root.mainloop()
