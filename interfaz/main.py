import tkinter as tk
from tkinter import filedialog, messagebox

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

from clustering_GUI import ClusteringApp


def iniciar_menu():
    def algoritmo1():
        # Crear la ventana secundaria para el Algoritmo 1
        new_window = tk.Toplevel(root)
        new_window.title("Algoritmo 1 - Regresión Lineal")
        new_window.geometry("500x500")  # Aumentar el tamaño para acomodar los widgets
        new_window.configure(bg='#e6f7ff')

        # Titulo de la ventana
        titulo = tk.Label(new_window, text="Regresión Lineal", font=("Helvetica", 18), bg='#e6f7ff', fg='black')
        titulo.pack(pady=20)

        # Descripción
        descripcion = tk.Label(new_window, text="Digite los datos para continuar", font=("Helvetica", 12), bg='#e6f7ff', fg='black')
        descripcion.pack(pady=10)

        # Botón para cargar CSV
        boton_cargar = tk.Button(new_window, text="Cargar CSV", bg='#ff3300', fg='black', width=20, height=2)
        boton_cargar.pack(pady=10)

        # Text widget para mostrar resultados del CSV cargado
        resultado_text = tk.Text(new_window, height=5, width=50)
        resultado_text.pack(pady=10)

        # Botón para entrenar el modelo
        boton_entrenar = tk.Button(new_window, text="Entrenar Algoritmo", bg='#00cc00', fg='black', width=20, height=2)
        boton_entrenar.pack(pady=10)

        # Mensaje de que el algoritmo se ha entrenado
        mensaje_entrenado = tk.Label(new_window, text="", font=("Helvetica", 12), bg='#e6f7ff', fg='green')
        mensaje_entrenado.pack(pady=10)

        # Input para predecir (ahora el usuario puede ingresar varios valores separados por comas)
        input_horas = tk.Entry(new_window, font=("Helvetica", 12))
        input_horas.pack(pady=10)
        input_horas.insert(tk.END, "Introduce las horas trabajadas (separadas por comas)")

        # Botón para predecir
        boton_predecir = tk.Button(new_window, text="Predecir", bg='#0066ff', fg='black', width=20, height=2)
        boton_predecir.pack(pady=10)

        # Resultado de la predicción
        resultado_prediccion = tk.Label(new_window, text="", font=("Helvetica", 12), bg='#e6f7ff', fg='blue')
        resultado_prediccion.pack(pady=10)

        # Botón para regresar al menú principal
        boton_regresar = tk.Button(new_window, text="Volver al Menú Principal", command=new_window.destroy, bg='#ff3300', fg='black', width=20, height=2)
        boton_regresar.pack(pady=20)

        # Algoritmo secuencial: todo dentro de una sola secuencia

        # Variables globales para el modelo y datos
        modelo = None
        datos = None

        # Función para cargar el archivo CSV
        def cargar_csv():
            nonlocal datos
            file_path = filedialog.askopenfilename(
                title="Selecciona un archivo CSV",
                filetypes=[("CSV files", "*.csv")]
            )
            if file_path:
                try:
                    datos = pd.read_csv(file_path)
                    resultado_text.delete('1.0', tk.END)  # Limpiar texto previo
                    resultado_text.insert(tk.END, f"Archivo cargado: {file_path}\n\n")
                    resultado_text.insert(tk.END, f"{datos.head()}\n")
                    resultado_text.insert(tk.END, f"\nColumnas: {list(datos.columns)}\n")
                    resultado_text.insert(tk.END, f"Filas totales: {len(datos)}")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")
            else:
                messagebox.showinfo("Cancelado", "No se seleccionó ningún archivo.")

        # Función para entrenar el modelo de regresión lineal
        def entrenar_algoritmo():
            nonlocal modelo, datos

            if datos is None:
                messagebox.showerror("Error", "Por favor, carga un archivo CSV primero.")
                return

            # Entrenamiento del modelo de regresión lineal
            regresion = LinearRegression()
            horas = datos['horas'].values.reshape((-1, 1))
            modelo = regresion.fit(horas, datos['ingreso'])

            # Mostrar mensaje de algoritmo entrenado
            mensaje_entrenado.config(text="Algoritmo entrenado con éxito!")

            # Mostrar coeficientes de la regresión
            print("Intersección (b)", modelo.intercept_)
            print("Pendiente (m)", modelo.coef_)

        # Función para predecir el ingreso basado en las horas
        def predecir():
            nonlocal modelo, datos

            if modelo is None:
                messagebox.showerror("Error", "Primero debes entrenar el algoritmo.")
                return

            # Obtener los valores de horas desde el input
            try:
                horas_input = input_horas.get().split(',')  # Dividir la entrada por comas
                horas_input = [float(hora.strip()) for hora in horas_input]  # Convertir a float y quitar espacios extra
            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa números válidos para las horas.")
                return

            # Realizar las predicciones para todas las horas ingresadas
            predicciones = modelo.predict([[hora] for hora in horas_input])

            # Mostrar la predicción
            resultado_prediccion.config(text=f"Predicciones: {', '.join([f'${p:.2f}' for p in predicciones])}")

            # Crear una nueva ventana para el gráfico
            fig_window = tk.Toplevel(new_window)
            fig_window.title("Gráfico de Predicción")
            fig_window.geometry("600x500")

            # Crear el gráfico con Matplotlib
            fig, ax = plt.subplots(figsize=(6, 4))

            # Graficar los datos reales y las predicciones
            ax.scatter(datos["horas"], datos["ingreso"], color="pink", label="Datos Reales")
            ax.scatter(horas_input, predicciones, color="red", label="Predicciones", zorder=5)
            ax.plot(datos["horas"], modelo.predict(datos["horas"].values.reshape(-1, 1)), color="black", label="Línea de Regresión")

            ax.set_xlabel("Horas trabajadas")
            ax.set_ylabel("Ingreso ($)")
            ax.grid(True)
            ax.legend()

            # Incrustar el gráfico en la nueva ventana con FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=fig_window)  # Crear el canvas con el gráfico
            canvas.draw()
            canvas.get_tk_widget().pack(pady=20)  # Añadir el canvas a la nueva ventana

        # Asociar las funciones a los botones
        boton_cargar.config(command=cargar_csv)
        boton_entrenar.config(command=entrenar_algoritmo)
        boton_predecir.config(command=predecir)


    def algoritmo2():
        new_window = tk.Toplevel(root)
        new_window.title("Algoritmo 2 - Regresión Logística")
        new_window.geometry("700x600")
        new_window.configure(bg='#e6f7ff')

        titulo = tk.Label(new_window, text="Regresión Logística", font=("Helvetica", 18), bg='#e6f7ff', fg='black')
        titulo.pack(pady=20)

        descripcion = tk.Label(new_window, text="Cargue un archivo CSV o ingrese valores manualmente", font=("Helvetica", 12), bg='#e6f7ff', fg='black')
        descripcion.pack(pady=10)

        model = None
        scaler = None
        data = None

        resultado_text = tk.Text(new_window, height=6, width=70)
        resultado_text.pack(pady=10)

        input_frame = tk.Frame(new_window, bg="#e6f7ff")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Edad:", bg="#e6f7ff").grid(row=0, column=0, sticky="e")
        edad_entry = tk.Entry(input_frame)
        edad_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Salario estimado:", bg="#e6f7ff").grid(row=1, column=0, sticky="e")
        salario_entry = tk.Entry(input_frame)
        salario_entry.grid(row=1, column=1)

        def cargar_csv():
            nonlocal data
            file_path = filedialog.askopenfilename(title="Selecciona un archivo CSV", filetypes=[("CSV files", "*.csv")])
            if file_path:
                try:
                    data = pd.read_csv(file_path)
                    columnas = list(data.columns)
                    if not {"Age", "EstimatedSalary", "Purchased"}.issubset(set(columnas)):
                        messagebox.showerror("Error", "El CSV debe contener las columnas 'Age', 'EstimatedSalary' y 'Purchased'")
                        return
                    resultado_text.delete("1.0", tk.END)
                    resultado_text.insert(tk.END, f"Archivo cargado: {file_path}\n\n")
                    resultado_text.insert(tk.END, f"{data.head()}\n")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")
            else:
                messagebox.showinfo("Cancelado", "No se seleccionó ningún archivo.")

        def entrenar_modelo():
            nonlocal model, data, scaler
            if data is None:
                messagebox.showerror("Error", "Primero debe cargar un archivo CSV.")
                return
            try:
                X = data[["Age", "EstimatedSalary"]]
                y = data["Purchased"]

                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)

                model = LogisticRegression(solver="liblinear", class_weight='balanced')
                model.fit(X_scaled, y)

                # Métricas de desempeño (opcional)
                y_pred = model.predict(X_scaled)
                print(classification_report(y, y_pred))

                messagebox.showinfo("Éxito", "Modelo entrenado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al entrenar el modelo:\n{e}")

        def predecir():
            nonlocal model, scaler
            if model is None or scaler is None:
                messagebox.showerror("Error", "Primero debes entrenar el modelo.")
                return
            try:
                edad = float(edad_entry.get())
                salario = float(salario_entry.get())

                X_new = scaler.transform([[edad, salario]])
                pred = model.predict(X_new)[0]

                resultado_text.delete("1.0", tk.END)
                resultado_text.insert(tk.END, f"\n🔍 Predicción para Edad={edad}, Salario={salario} ➤ {'🟢 Comprará (1)' if pred == 1 else '🔴 No comprará (0)'}\n")

                # Mostrar en gráfico
                fig_window = tk.Toplevel(new_window)
                fig_window.title("Gráfico con Predicción")
                fig_window.geometry("800x700")

                fig, ax = plt.subplots(figsize=(6, 4))
                for etiqueta in data["Purchased"].unique():
                    subset = data[data["Purchased"] == etiqueta]
                    ax.scatter(subset["Age"], subset["EstimatedSalary"], label=f"Clase {etiqueta}", alpha=0.7)

                ax.scatter(edad, salario, color="red", s=100, label="Predicción", edgecolors="black", zorder=10)
                ax.set_xlabel("Edad")
                ax.set_ylabel("Salario Estimado")
                ax.set_title("Visualización de Datos y Predicción")
                ax.legend()
                ax.grid(True)

                canvas = FigureCanvasTkAgg(fig, master=fig_window)
                canvas.draw()
                canvas.get_tk_widget().pack(pady=20)

            except ValueError:
                messagebox.showerror("Error", "Por favor, ingresa valores válidos para Edad y Salario.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def mostrar_grafico():
            nonlocal data
            if data is None:
                messagebox.showerror("Error", "Primero debe cargar un archivo CSV.")
                return
            fig_window = tk.Toplevel(new_window)
            fig_window.title("Gráfico de Regresión Logística")
            fig_window.geometry("800x700")
            fig, ax = plt.subplots(figsize=(6, 4))
            for etiqueta in data["Purchased"].unique():
                subset = data[data["Purchased"] == etiqueta]
                ax.scatter(subset["Age"], subset["EstimatedSalary"], label=f"Clase {etiqueta}", alpha=0.7)

            ax.set_xlabel("Edad")
            ax.set_ylabel("Salario Estimado")
            ax.set_title("Visualización de Datos")
            ax.legend()
            ax.grid(True)

            canvas = FigureCanvasTkAgg(fig, master=fig_window)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=20)

        # Botones
        tk.Button(new_window, text="Cargar CSV", command=cargar_csv, width=25, bg='#ff9900').pack(pady=5)
        tk.Button(new_window, text="Entrenar Modelo", command=entrenar_modelo, width=25, bg='#00cc00').pack(pady=5)
        tk.Button(new_window, text="Predecir", command=predecir, width=25, bg='#0066ff').pack(pady=5)
        tk.Button(new_window, text="Mostrar Gráfico", command=mostrar_grafico, width=25, bg='#9900cc', fg='white').pack(pady=5)

#Clustering

    def algoritmo3():
        new_window = tk.Toplevel(root)
        new_window.title("Algoritmo 3 - Clustering")
        new_window.geometry("600x400")
        new_window.configure(bg = "#e6f7ff")

        app = ClusteringApp(new_window)

        
        boton_regresar = tk.Button(new_window, text="Volver al Menú Principal", command=new_window.destroy, bg='#ff3300', fg='black', width=20, height=2)
        boton_regresar.pack(pady=20)


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

    titulo = tk.Label(root, text="Bienvenido al programa, elija un opcion", font=("Arial", 34), bg='#1a1a4b', fg='white')
    titulo.grid(row=0, column=0, columnspan=2, pady=20, sticky="nsew")

    frame = tk.Frame(root, bg='#1a1a4b')
    frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

    # Configurar las filas y columnas del marco
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # Botones dentro del marco
    boton1 = tk.Button(frame, text="Regresión Linear", command=algoritmo1, bg='#0099cc', fg='black')
    boton1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    boton2 = tk.Button(frame, text="Regresión Logistica", command=algoritmo2, bg='#663399', fg='black')
    boton2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    boton3 = tk.Button(frame, text="Clustering", command=algoritmo3, bg='#ffcc00', fg='black')
    boton3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    boton4 = tk.Button(frame, text="Salir", command=salir, bg='#ff3300', fg='black')
    boton4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    root.mainloop()


iniciar_menu()
