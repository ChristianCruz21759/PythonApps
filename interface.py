import tkinter as tk
from tkinter import filedialog

def open_file():
    file_path = filedialog.askopenfilename()
    print("Selected filepath:", file_path)

def button2_click():
    print("Button 2 was clicked")

# Create the main window
window = tk.Tk()
window.geometry("400x200")
window.title("Análisis Modos de Falla")

# Create the buttons
button1 = tk.Button(window, text="Selecciona el archivo a analizar", command=open_file)
button2 = tk.Button(window, text="Actualizar los datos", command=button2_click)

# Place the buttons in the window
button1.place(x=30, y=50)
button2.place(x=30, y=85)

# Start the event loop
window.mainloop()
