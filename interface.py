import tkinter as tk
from tkinter import filedialog

def open_file():
    file_path = filedialog.askopenfilename()
    print("Selected filepath:", file_path)

def button2_click():
    print("Button 2 was clicked")

# Create the main window
window = tk.Tk()
window.title("Interface with Buttons")

# Create the buttons
button1 = tk.Button(window, text="Button 1", command=open_file)
button2 = tk.Button(window, text="Button 2", command=button2_click)

# Place the buttons in the window
button1.pack()
button2.pack()

# Start the event loop
window.mainloop()
