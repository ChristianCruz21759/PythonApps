import tkinter as tk
from tkinter import ttk

colors = ["red", "blue", "green", "orange", "yellow", "red"]

def scroll_function(*args):
    canvas.configure(scrollregion=canvas.bbox("all"), width=200, height=200)

root = tk.Tk()
root.geometry("400x300")

# Crear un contenedor de frames
canvas = tk.Canvas(root, bg="lightgrey")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

canvas2 = tk.Canvas(root, bg="lightblue")
canvas2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", scroll_function)

# Crear el frame principal dentro del canvas
frame = tk.Frame(canvas, bg="pink")
canvas.create_window((0, 0), window=frame, anchor="nw")

num_frames = 6

for i in range(num_frames):

    # Crear tres frames internos dentro del frame principal
    inner_frames = tk.Frame(frame, bg=colors[i], width=200, height=200)

    # Colocar los frames internos dentro del frame principal
    inner_frames.grid(row=i, column=0, padx=10, pady=10)
    
root.mainloop()
