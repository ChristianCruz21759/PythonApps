import tkinter as tk
from tkinter import filedialog
import pandas as pd

import nlp_functions
import os

hiddenimports = ['scikit-learn', 'sklearn']

df = None

def open_file():
    global df
    file_path = filedialog.askopenfilename()
    print("Selected filepath:", file_path)
    df = nlp_functions.read_xlsx(file_path)

def button2_click():
    print("Analisis Top Reasons")
    print(nlp_functions.getData_top4(df, 2, 4))

def button3_click():
    print("Analisis NLP")
    data, keywords = nlp_functions.getData_topics(df, 1, 5, 3)
    print(data)
    print(keywords)

# Create the main window
window = tk.Tk()
window.geometry("1000x800")
window.title("Análisis Modos de Falla")

# Create the buttons
button1 = tk.Button(window, text="Selecciona el archivo a analizar", command=open_file)
button2 = tk.Button(window, text="Analisis Top Reasons", command=button2_click)
button3 = tk.Button(window, text="Analisis NLP", command=button3_click)

# Place the buttons in the window
button1.place(x=30, y=50)
button2.place(x=30, y=85)
button3.place(x=30, y=120)

# Start the event loop
window.mainloop()



