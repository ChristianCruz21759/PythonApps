import tkinter as tk
from tkinter import ttk

def create_widgets():
    # Marco izquierdo
    left_frame = tk.Frame(root, bg="lightblue", width=200, height=400)
    left_frame.grid(row=0, column=0, padx=10, pady=10)

    # Columna para los botones
    button_column = tk.Frame(left_frame, bg="lightyellow")
    button_column.grid(row=0, column=0, padx=5, pady=5)

    # Botones en la columna izquierda
    tk.Button(button_column, text="Botón 1").pack()
    tk.Button(button_column, text="Botón 2").pack()
    tk.Button(button_column, text="Botón 3").pack()

    # Columna para los cuadros de entrada de números
    entry_column = tk.Frame(left_frame, bg="lightgreen")
    entry_column.grid(row=0, column=1, padx=5, pady=5)

    empty_frame1 = tk.Frame(left_frame, bg="pink", height=100, width=100)
    empty_frame1.grid(row=1, column=0, columnspan=2)

    # Cuadros de entrada de números en la columna derecha
    for i in range(3):
        entry = tk.Entry(
        entry_column)
        entry.pack()



    # Marco derecho
    right_frame = tk.Frame(root, bg="lightgreen", width=800, height=400)
    right_frame.grid(row=0, column=1, padx=10, pady=10)

    # Canvas para la columna derecha
    canvas = tk.Canvas(right_frame, bg="lightgrey", width=800, height=400)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Barra de desplazamiento vertical
    scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    # Configurar el canvas para que se desplace con la barra de desplazamiento
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Marco interior para contener los marcos vacíos
    inner_frame = tk.Frame(canvas, bg="lightgrey")
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # Crear marcos vacíos en el marco interior
    for i in range(3):
        row_frame = tk.Frame(inner_frame, bg="white", width=200, height=100, padx=5, pady=5)
        row_frame.grid(row=i, column=0, padx=5, pady=5)
        row_frame = tk.Frame(inner_frame, bg="white", width=200, height=100, padx=5, pady=5)
        row_frame.grid(row=i, column=1, padx=5, pady=5)
        row_frame = tk.Frame(inner_frame, bg="white", width=200, height=100, padx=5, pady=5)
        row_frame.grid(row=i, column=2, padx=5, pady=5)

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz con dos columnas")

# Cambiar el tamaño de la ventana
root.geometry("1000x500")

# Llamar a la función para crear widgets
create_widgets()

# Iniciar el bucle principal de la aplicación
root.mainloop()
