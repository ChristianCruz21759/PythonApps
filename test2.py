import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import nlp_functions
from matplotlib.figure import Figure 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 

colors = ['#02007b', '#7f0075', '#bf0061', '#e91647', '#fe6829', '#ffa600', '#C2C8E3']
# cambiar esto por dios
colors2 = ["red", "blue", "green", "orange", "yellow", "red"]

w = 1440
h = 750

def open_file():
    global df
    file_path = filedialog.askopenfilename()
    print("Selected filepath:", file_path)  
    df = nlp_functions.read_xlsx(file_path)

def scroll_function(*args):
    canvas.configure(scrollregion=canvas.bbox("all"))

def graph_nlp():
    
    global canvas

    num_reasons = int(num_reasons_btn.get())
    num_keywords = int(num_keywords_btn.get())
    num_clusters = int(num_clusters_btn.get())

    # Canvas para la columna derecha
    canvas = tk.Canvas(root, bg="lightgrey")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)    

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", scroll_function)

    # Marco interior para contener los marcos vacíos
    inner_frame = tk.Frame(canvas, bg="pink")
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    for i in range(num_reasons):

        data, keywords = nlp_functions.getData_topics(df, num_reasons, i+1, num_clusters, num_keywords)
        
        print(data)

        fig = Figure(figsize=(4.5,3), dpi=100)
        fig_canvas = FigureCanvasTkAgg(fig, inner_frame)
            
        axes = fig.add_subplot()
        axes.bar(data[0], data[1])
        axes.set_ylim(0, max(data[1])*1.100)    
        
        fig_canvas.get_tk_widget().grid(row=i, column=0)

        t = tk.Text(inner_frame, width=65, height=15)
        for j in range(num_clusters):

            try:
                topic_str = data[0][j]
            except IndexError:
                break

            t.insert(END, topic_str + ": " + str(keywords[j]) +"\n")
            t.grid(row=i, column=1, pady=10)
        
def button2_click():

    global left_frame

    buf = int(num_reasons_btn.get())

    print("Analisis Top Reasons")
    data = nlp_functions.getData_top4(df, 2, buf)

    fig = Figure(figsize=(4.05,5), dpi=100)
    fig_canvas = FigureCanvasTkAgg(fig, left_frame)

    toolbar = NavigationToolbar2Tk(fig_canvas, left_frame, pack_toolbar=False)
    toolbar.update()

    explode = [0] * len(data[0]) # only "explode" the 1st slice
    explode[0] = 0.1

    axes = fig.add_subplot()
    axes.pie(data[1], autopct='%1.1f%%', pctdistance=1.2, explode=explode, startangle=90, colors=colors)

    box = axes.get_position()
    axes.set_position([box.x0, box.y0 - box.height * buf/20,
                 box.width, box.height])

    axes.legend(labels=data[0], loc="upper center", bbox_to_anchor=(0.5, 1 + buf /10))

    fig_canvas.get_tk_widget().grid(row=2, column=0, columnspan=3)
    toolbar.grid(row=3, column=0, columnspan=3)

def button3_click():
    print("Analisis NLP")
    # print(keywords)
    graph_nlp()



def create_widgets():

    global left_frame

    # Marco izquierdo
    left_frame = tk.Frame(root, bg="lightblue")
    # left_frame.grid(row=0, column=0, padx=10, pady=10)
    left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

    title = tk.Label(left_frame, bg="pink", height=2, width=25, text="Analisis Modos de Falla", font=("Arial", 25))
    title.grid(row=0, column=0, padx=5, pady=5, columnspan=3)

    # Columna para los botones
    button_column = tk.Frame(left_frame, bg="lightyellow")
    button_column.grid(row=1, column=0, padx=5, pady=5)

    # Botones en la columna izquierda
    tk.Button(button_column, text="Escoger archivo", command=open_file).pack()
    tk.Button(button_column, text="Analisis de Razones", command=button2_click).pack()
    tk.Button(button_column, text="Analisis NLP",command=button3_click).pack()
    
    # Columna para las labels
    label_column = tk.Frame(left_frame, bg="lightyellow")
    label_column.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(label_column, text="Razones:").pack()
    tk.Label(label_column, text="Clusters:").pack()
    tk.Label(label_column, text="Keywords:").pack()

    # Columna para los cuadros de entrada de números
    entry_column = tk.Frame(left_frame, bg="lightgreen")
    entry_column.grid(row=1, column=2, padx=5, pady=5)

    global num_reasons_btn
    global num_clusters_btn
    global num_keywords_btn


    num_reasons_btn = tk.StringVar(value=4)
    num_clusters_btn = tk.StringVar(value=5)
    num_keywords_btn = tk.StringVar(value=4)

    num_var = [num_reasons_btn, num_clusters_btn, num_keywords_btn]

    # Cuadros de entrada de números en la columna derecha
    for i in range(3):
        entry = tk.Spinbox(
        entry_column, from_=3, to=6, textvariable=num_var[i])
        entry.pack()

    # Marco derecho
    # right_frame = tk.Frame(root, bg="lightgreen", width=1000-100)
    # # right_frame.grid(row=0, column=1, padx=0, pady=10)
    # right_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

    # # Canvas para la columna derecha
    # canvas = tk.Canvas(root, bg="lightgrey")
    # canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)    

    # canvas.configure(yscrollcommand=scrollbar.set)
    # canvas.bind("<Configure>", scroll_function)

    # # Marco interior para contener los marcos vacíos
    # inner_frame = tk.Frame(canvas, bg="pink")
    # canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # num_frames = 6

    # for i in range(num_frames):

    #     # Crear tres frames internos dentro del frame principal
    #     inner_frames = tk.Frame(inner_frame, bg=colors2[i], width=200, height=200)

    #     # Colocar los frames internos dentro del frame principal
    #     inner_frames.grid(row=i, column=0, padx=10, pady=10)


# Crear la ventana principal
root = tk.Tk()
root.title("Analisis Modos de Falla - Manufactura")

# Cambiar el tamaño de la ventana
root.geometry("1440x750")
root.resizable(0, 0)

# Llamar a la función para crear widgets
create_widgets()

# Iniciar el bucle principal de la aplicación
root.mainloop()


