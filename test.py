import tkinter as tk

def boton1_click():
    print("Botón 1 fue clickeado")

def boton2_click():
    print("Botón 2 fue clickeado")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz con botones")

# Crear los botones
boton1 = tk.Button(ventana, text="Botón 1", command=boton1_click)
boton2 = tk.Button(ventana, text="Botón 2", command=boton2_click)

# Ubicar los botones en la ventana
boton1.pack()
boton2.pack()

# Iniciar el bucle de eventos
ventana.mainloop()
