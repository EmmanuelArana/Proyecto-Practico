import tkinter as tk

def iniciar_menu():
    def algoritmo1():
        new_window = tk.Toplevel(root)
        new_window.title("Algoritmo 1 - Regresión Lineal")
        new_window.geometry("400x300")
        new_window.configure(bg='#e6f7ff')

        titulo = tk.Label(new_window, text="Regresión Lineal", font=("Helvetica", 18), bg='#e6f7ff', fg='black')
        titulo.pack(pady=20)

        descripcion = tk.Label(new_window, text="Digite los datos para continuar", font=("Helvetica", 12), bg='#e6f7ff', fg='black')
        descripcion.pack(pady=10)

        boton_regresar = tk.Button(new_window, text="Volver al Menú Principal", command=new_window.destroy, bg='#ff3300', fg='black', width=20, height=2)
        boton_regresar.pack(pady=20)

    def algoritmo2():
        print("Algoritmo 2")

    def algoritmo3():
        print("Algoritmo 3")

    def salir():
        root.destroy()

    root = tk.Tk()
    root.title("Inicio")
    root.geometry("600x400")  # Ventana inicial más grande
    root.configure(bg='#1a1a4b')

    # Configurar filas y columnas para que sean proporcionales
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    titulo = tk.Label(root, text="Inicio", font=("Helvetica", 24), bg='#1a1a4b', fg='white')
    titulo.grid(row=0, column=0, columnspan=2, pady=20, sticky="nsew")

    frame = tk.Frame(root, bg='#1a1a4b')
    frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

    # Configurar las filas y columnas del marco
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # Botones dentro del marco
    boton1 = tk.Button(frame, text="Algoritmo 1", command=algoritmo1, bg='#0099cc', fg='black')
    boton1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    boton2 = tk.Button(frame, text="Algoritmo 2", command=algoritmo2, bg='#663399', fg='black')
    boton2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    boton3 = tk.Button(frame, text="Algoritmo 3", command=algoritmo3, bg='#ffcc00', fg='black')
    boton3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    boton4 = tk.Button(frame, text="Salir", command=salir, bg='#ff3300', fg='black')
    boton4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    root.mainloop()


