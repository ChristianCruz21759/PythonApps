import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import nlp_functions

from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 

w = 1440
h = 810

def open_file():
    global df
    file_path = filedialog.askopenfilename()
    print("Selected filepath:", file_path)  
    df = nlp_functions.read_xlsx(file_path)

def button2_click():

    global left_frame

    buf = int(num_reasons.get())

    print("Analisis Top Reasons")
    data = nlp_functions.getData_top4(df, 2, buf)

    fig = Figure(figsize=(4.05,5), dpi=100)
    fig_canvas = FigureCanvasTkAgg(fig, left_frame)

    toolbar = NavigationToolbar2Tk(fig_canvas, left_frame, pack_toolbar=False)
    toolbar.update()


    axes = fig.add_subplot()
    axes.pie(data[1], autopct='%1.1f%%', pctdistance=1.2)

    box = axes.get_position()
    axes.set_position([box.x0, box.y0 - box.height * buf/20,
                 box.width, box.height])

    axes.legend(labels=data[0], loc="upper center", bbox_to_anchor=(0.5, 1 + buf /10))

    fig_canvas.get_tk_widget().grid(row=2, column=0, columnspan=2)
    toolbar.grid(row=3, column=0, columnspan=2)

def button3_click():
    print("Analisis NLP")
    data, keywords = nlp_functions.getData_topics(df, 1, 5, 3)
    print(data)
    print(keywords)



def create_widgets():

    global left_frame

    # Marco izquierdo
    left_frame = tk.Frame(root, bg="lightblue", width=440, height=h-20)
    left_frame.grid(row=0, column=0, padx=10, pady=10)

    title = tk.Label(left_frame, bg="pink", height=5, width=55, text="Analisis Modos de Falla")
    title.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

    # Columna para los botones
    button_column = tk.Frame(left_frame, bg="lightyellow")
    button_column.grid(row=1, column=0, padx=5, pady=5)

    # Botones en la columna izquierda
    tk.Button(button_column, text="Escoger archivo", command=open_file).pack()
    tk.Button(button_column, text="Analisis de Razones", command=button2_click).pack()
    tk.Button(button_column, text="Analisis NLP",command=button3_click).pack()

    # Columna para los cuadros de entrada de números
    entry_column = tk.Frame(left_frame, bg="lightgreen")
    entry_column.grid(row=1, column=1, padx=5, pady=5)

    # empty_frame1 = FigureCanvasTkAgg(left_frame, bg="pink", height=h/2, width=h/2)
    # empty_frame1.grid(row=2, column=0, columnspan=2)

    global num_reasons

    num_reasons = tk.StringVar(value=4)
    num_keywords = tk.StringVar(value=4)
    num_clusters = tk.StringVar(value=4)

    num_var = [num_reasons, num_keywords, num_clusters]

    # Cuadros de entrada de números en la columna derecha
    for i in range(3):
        entry = tk.Spinbox(
        entry_column, from_=3, to=6, textvariable=num_var[i])
        entry.pack()

    # Marco derecho
    right_frame = tk.Frame(root, bg="lightgreen", width=1000-10, height=h-20)
    right_frame.grid(row=0, column=1, padx=0, pady=10)

    # Canvas para la columna derecha
    canvas = tk.Canvas(right_frame, bg="lightgrey", width=1000-10, height=h-20)
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
    for i in range(6):
        row_frame = tk.Frame(inner_frame, bg="white", width=485, height=250, padx=5, pady=5)
        row_frame.grid(row=i, column=0, padx=5, pady=5)
        row_frame = tk.Frame(inner_frame, bg="white", width=485, height=250, padx=5, pady=5)
        row_frame.grid(row=i, column=1, padx=5, pady=5)
        # row_frame = tk.Frame(inner_frame, bg="white", width=320, height=200, padx=5, pady=5)
        # row_frame.grid(row=i, column=2, padx=5, pady=5)

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz con dos columnas")

# Cambiar el tamaño de la ventana
root.geometry("1440x810")
root.resizable(0, 0)

# Llamar a la función para crear widgets
create_widgets()

# Iniciar el bucle principal de la aplicación
root.mainloop()


