import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image

# Create a Tkinter root window with a hidden dialog
root = tk.Tk()
root.withdraw()

# Use file dialog to select input file
file_path = filedialog.askopenfilename()

# Check if input file is a .png
if not file_path.lower().endswith('.png'):
    print('Input file must be in .png format')
    exit()

# Create a PIL Image object from the input file
img = Image.open(file_path)

# Create a new file name for the .ico file
file_name = os.path.splitext(os.path.basename(file_path))[0]
ico_file_path = filedialog.asksaveasfilename(initialfile=file_name, defaultextension=".ico")

# Save the PIL Image object as an .ico file using the file name
img.save(ico_file_path, format='ICO')
