# ==========================================================
# Apex Global Mobility S.A.
# Analisis Modos de Falla para sistema ATLAS
# Desarrollado por: Christian Cruz
# Fecha: 14/5/2024
# ==========================================================

# --------- TO DO LIST ---------
# max df and min df check value error
# delete console from appearing --noconsole on creating app
# delete clean button

# ------ DEFINICION DE LIBRERIAS -----------------------------------------

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import nltk
import nlp_functions
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from textwrap import wrap

# ------ DEFINICION DE VARIABLES GLOBALES ----------------------------------

# Colores para graficas
colors = ['#02007b', '#7f0075', '#bf0061', '#e91647', '#fe6829', '#ffa600', '#c2c8e3']

# Tamaño de la ventana
winWidth = 1440        # Largo ventana
winHeight = 750         # Altura ventana

# Lista de opciones
optionsList = ["LEF", "IndExt"]

# ------ DEFINICION DE FUNCIONES -----------------------------------------

# Funcion para abrir el archivo seleccionado - Boton 1
def open_file():
    global df
    # Obtenemos el nombre del archivo a abrir
    file_path = filedialog.askopenfilename()
    # Cargamos el archivo excel en nuestro df
    df = nlp_functions.read_xlsx(file_path)
    # Cambiar estado de botones
    if file_path == '':
        b2['state'] = 'disabled'
        messagebox.showinfo("Estado del archivo", "Archivo cargado incorrectamente.")
    else:
        b2['state'] = 'normal'
        messagebox.showinfo("Estado del archivo", "Archivo cargado correctamente.")

# Funcion para limpiar las graficas
def clear():
    # Buscamos si el objeto existe para borrar todo
    try:
        fig_canvas1
    except NameError:
        print("error")
    else:
        fig_canvas1.get_tk_widget().destroy()

# Funcion para actualizar las scroll bars
def scroll_function(*args):
    right_frame.configure(scrollregion=right_frame.bbox("all"))
    
def updateScrollRegion():
	right_frame.update_idletasks()
	right_frame.config(scrollregion=inner_frame.bbox())

# ------ FUNCIONES PARA LOS WIDGETS ------------------------------------------------

# BOTON 1 - Limpiamos -> Abrimos archivo -> Verificamos botones
def button1_click():
    clear()
    open_file()
    switch()

# BOTON 2 - Limpiamos -> Graficamos razones -> Graficamos NLP y SKU -> Verificamos botones
def button2_click():
    clear()
    graph_reasons()
    graph_nlp()
    switch()

# BOTON 3 - Limpiamos -> Verificamos botones -> Disable todos los botones
def button3_click():
    clear()
    switch()
    b2['state'] = 'disabled'
    b3['state'] = 'disabled'

# CALLBACK DROPDOWN MENU
def my_callback(var, index, mode):
    switch()

# SWITCH PARA ENABLE/DISABLE BOTONES
def switch():
    if option_value.get().startswith('Selecciona'):
        b1['state'] = 'disabled'
    else:
        b1['state'] = 'normal'

# ------ FUNCIONES PARA GRAFICAR ---------------------------------------------

# --- FUNCION PARA GRAFICAR RAZONES PRINCIPALES ------------------------------

def graph_reasons():        # Funcion para graficar las razones principales en un pie chart

    global titles
    global fig_canvas1
    # global toolbar
    global new_df

    # Obtenemos el numero de razones a graficar
    buf = int(num_reasons_btn.get())    

    # Obtenemos la super razon
    option = option_value.get()

    if option == 'IndExt':
        tags = ['Indisponibilidad Externa']
    elif option == 'LEF':
        tags = ['Paradas Electromecanicas', 'Paradas Operacionales']

    new_df = df[df['Super Reason'].isin(tags)]                 # Obtenemos los registros de esa super razon
    data = nlp_functions.getData_top(new_df, 2, buf)          # Obtenemos data de las razones
    titles = data[0]                                           # Guardamos los titulos como variable global
    fig = Figure(figsize=(4.05, 5), dpi=100)                   # Creamos figura
    fig_canvas1 = FigureCanvasTkAgg(fig, left_frame)

    # toolbar = NavigationToolbar2Tk(
    #     fig_canvas1, left_frame, pack_toolbar=False)  # Creamos toolbar
    # toolbar.update()

    explode = [0] * len(data[0])  # Razon 1 resaltada
    explode[0] = 0.1

    axes = fig.add_subplot()        # Creamos la grafica
    axes.pie(data[1], autopct='%1.1f%%', pctdistance=1.2, explode=explode, startangle=90, colors=colors)
    box = axes.get_position()       # Obtenemos tamaño y posicion de la grafica
    axes.set_position([box.x0, box.y0 - box.height*buf/20, box.width, box.height])
    axes.legend(labels=data[0], loc="upper center", bbox_to_anchor=(0.5, 1 + buf / 10)) # Colocamos la leyenda

    # Colocamos la figura en el grid
    fig_canvas1.get_tk_widget().grid(row=2, column=0, columnspan=4, pady=12)
    # Colocamos la toolbar en el grid
    # toolbar.grid(row=3, column=0, columnspan=4)

# --- FUNCIONES PARA GRAFICAR ANALISIS NLP Y SKU ----------------------------------------------

def graph_nlp():

    global inner_frame

    # Obtenemos configuraciones de los spinbox
    num_reasons = int(num_reasons_btn.get())
    num_keywords = int(num_keywords_btn.get())
    num_clusters = int(num_clusters_btn.get())

    # Marco interior para contener los marcos vacíos
    # inner_frame = tk.Frame(right_frame, bg='white', padx=5, pady=5)
    # right_frame.create_window((0, 0), window=inner_frame, anchor="nw")

    # Realizamos el numero de analisis NLP para el numero de razones (si es posible)
    for i in range(num_reasons):

        # Obtenemos los datos de NLP y los guardamos en variables temporales
        data, keywords = nlp_functions.getData_topics(
            new_df, num_reasons, i+1, num_clusters, num_keywords, stopwords_es)
        values = [float(x) for x in data[1]]

        # Creamos la fila donde iran nuestas graficas
        graph_frame = tk.Frame(inner_frame, bg=colors[i])
        graph_frame.grid(row=i, column=0)

        # Creamos la figura y el grafico de barras
        fig = Figure(figsize=(4.5, 4), dpi=100)
        fig_canvas = FigureCanvasTkAgg(fig, graph_frame)
        axes = fig.add_subplot()
        axes.bar(data[0], values, color=colors[i])
        axes.set_ylim(0, max(values)*1.250)
        axes.set_title(titles[i])

        # Colocamos la grafica en la fila
        fig_canvas.get_tk_widget().grid(row=0, column=0, pady=10)

        # Agregar etiquetas con las horas sobre cada barra
        for k, v in enumerate(values):
            try:
                axes.text(k, v+max(values)/7, f'{data[1][k]} h', ha='center', va='center', weight=200)
                axes.text(k, v+max(values)/14, f'{data[2][k]}%', ha='center', va='center', weight=200)
            except KeyError:
                break

        # Creamos cuadro con total de horas
        axes.text(k-1*(k+1)/4, max(values), f'Total de horas: \n{round(
            sum(values), 2)} h', bbox=dict(facecolor='white', alpha=0.5), fontsize='medium')

        # Incluimos las keywords como label en la fila
        var = StringVar()
        t = tk.Label(graph_frame, width=50, font='Arial 13', textvariable=var, anchor=tk.W, justify="left", padx=5, bg='white')
        buf = ''
        for j in range(len(data[0])):
            buf = buf + data[0][j] + ": " + str(keywords[j]) + "\n"
        var.set(buf)
        # Colocamos la label en la fila
        t.grid(row=0, column=1, pady=10, sticky='NS')

        # Obtenemos data SKu y se guarda en variables temporales
        data2 = nlp_functions.getData_sku(new_df, num_reasons, i+1, 4)
        values = [float(x) for x in data2[1]]

        # Creamos figura y graficas
        fig = Figure(figsize=(7, 4), dpi=100)
        fig_canvas = FigureCanvasTkAgg(fig, graph_frame)
        axes = fig.add_subplot()
        axes.barh(data2[0], values, color=colors[i])
        axes.set_xlim(0, max(values)*1.3)
        axes.set_title("SKU " + titles[i])
        wrapped_labels = ['\n'.join(wrap(l, 10)) for l in data2[0]] 
        axes.set_yticklabels(wrapped_labels)
        
        # Colocamos grafica en la fila
        fig_canvas.get_tk_widget().grid(row=0, column=2)

        # Agregar etiquetas con las horas sobre cada barra
        for k, v in enumerate(values):
            try:
                axes.text(v+max(values)/14, k, f'{data2[1][k]}h', ha='center', va='center', weight=200)
                axes.text(v+max(values)/5, k, f'{data2[2][k]}%', ha='center', va='center', weight=200)
            except KeyError:
                break
    updateScrollRegion()
    # Creamos las scrollbars y las configuramos
    # scrollbar_y = ttk.Scrollbar(root, orient="vertical", command=right_frame.yview)
    # scrollbar_y.grid(row=0, column=2, sticky='NS')

    # scrollbar_x = ttk.Scrollbar(root, orient="horizontal", command=right_frame.xview)
    # scrollbar_x.grid(row=1, column=1, columnspan=2, sticky='WE')

    # right_frame.configure(yscrollcommand=scrollbar_y.set)
    # right_frame.configure(xscrollcommand=scrollbar_x.set)
    # right_frame.bind("<Configure>", scroll_function)

    b3['state'] = 'normal'

# ------ FUNCION PARA CREAR WIDGETS ----------------------------------------------


def create_widgets():

    global left_frame           # Marco izquierdo
    global right_frame          # Marco derecho (canvas)
    global HorizontalScrollBar
    global VerticalScrollBar
    global inner_frame

    # Marco izquierdo
    left_frame = tk.Frame(root, bg="lightblue", highlightbackground='#646464', highlightthickness=2)
    left_frame.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky='NS')

    # Titulo (0,0-2)
    title = tk.Label(left_frame, bg="pink", height=2, width=25, text="Analisis Modos de Falla", font=("Arial", 25))
    title.grid(row=0, column=0, padx=5, pady=5, columnspan=4)

    # Columna para los botones (1,0)
    button_column = tk.Frame(left_frame)
    button_column.grid(row=1, column=0, padx=5, pady=5)

    global b1
    global b2
    global b3

    # Botones en la columna izquierda
    b1 = tk.Button(button_column, text="Escoger archivo", command=button1_click)
    b1.pack()
    b1['state'] = 'disabled'

    b2 = tk.Button(button_column, text="Analizar archivo", command=button2_click)
    b2.pack()
    b2['state'] = 'disabled'
    b3 = tk.Button(button_column, text="Limpiar", command=button3_click)
    b3.pack()
    b3['state'] = 'disabled'

    # Columna para lista (listbox) (1,1)
    optionsList_column = tk.Frame(left_frame)
    optionsList_column.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(optionsList_column, text="Area:").pack()

    # Leer los valores del option menu y volverlos globales
    global option_value

    option_value = tk.StringVar(root)
    option_value.trace_add('write', my_callback)
    option_value.set("Selecciona \n una opcion")

    option_menu = tk.OptionMenu(optionsList_column, option_value, *optionsList)
    option_menu.pack()

    # Columna para las labels (1,2)
    label_column = tk.Frame(left_frame)
    label_column.grid(row=1, column=2, padx=5, pady=5)

    # Labels para los botones
    tk.Label(label_column, text="Razones:").pack()
    tk.Label(label_column, text="Clusters:").pack()
    tk.Label(label_column, text="Keywords:").pack()

    # Columna para los cuadros de entrada de números (1,3)
    entry_column = tk.Frame(left_frame)
    entry_column.grid(row=1, column=3, padx=5, pady=5)

    # Leer valores de los spinbox y volverlos globales
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
        
    # Crear elementos para el marco derecho
    right_frame = tk.Canvas(root, height=winHeight-50, width=winWidth-562, bg='white')    
    inner_frame = tk.Frame(right_frame)
    HorizontalScrollBar = tk.Scrollbar(root)
    VerticalScrollBar = tk.Scrollbar(root)
    
    # Configurar scrollbars 
    right_frame.config(xscrollcommand=HorizontalScrollBar.set,yscrollcommand=VerticalScrollBar.set, highlightthickness=0)
    HorizontalScrollBar.config(orient=tk.HORIZONTAL, command=right_frame.xview)
    VerticalScrollBar.config(orient=tk.VERTICAL, command=right_frame.yview)
    
    # Colocar objetos en el root
    VerticalScrollBar.grid(row=0, column=2, sticky='NS')
    HorizontalScrollBar.grid(row=1, column=1, columnspan=2, sticky='WE')
    right_frame.grid(row=0, column=1, padx=10, pady=10)
    
    # Crear un objeto de ventana para poder scrollear dentro de el, usamos inner frame como el objeto 
    right_frame.create_window(0, 0, window=inner_frame, anchor=tk.NW)

# ------ CODIGO PARA CREAR LA VENTANA PRINCIPAL/MAIN LOOP -----------------

# Crear la ventana principal
root = tk.Tk()
root.title("Analisis Modos de Falla - Manufactura")
root.config(background='white')

# Cambiar el tamaño de la ventana
winSize = str(winWidth)+'x'+str(winHeight)
root.geometry(winSize)
root.resizable(0, 0)

# Incluir logo como icono
pic = PhotoImage(file="apex logo.png")
root.iconphoto(False, pic)

# Llamar a la función para crear widgets
create_widgets()

# Descargar recursos para NLTK
nltk.download('punkt')
nltk.download('stopwords')
# Obtener stopwords en español
stopwords_es = nltk.corpus.stopwords.words('spanish')
# Agregar nuestras propias stopwords
my_stopwords = ['dee', 'agr', 'een', 'nan', 'iw', '']
stopwords_es.extend(my_stopwords)

# Iniciar el bucle principal de la aplicación
root.mainloop()
