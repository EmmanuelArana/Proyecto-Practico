#Código para meter un archivo a tkinter
#Para entrenar al algoritmo
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def cargar_csv():
    file_path = filedialog.askopenfilename(
        title="Selecciona un archivo CSV",
        filetypes=[("CSV files", "*.csv")]
    )
    if file_path:
        try:
            df = pd.read_csv(file_path)
            resultado_text.delete('1.0', tk.END)  # Limpiar texto previo
            resultado_text.insert(tk.END, f"Archivo cargado: {file_path}\n\n")
            resultado_text.insert(tk.END, f"{df.head()}\n")
            resultado_text.insert(tk.END, f"\nColumnas: {list(df.columns)}\n")
            resultado_text.insert(tk.END, f"Filas totales: {len(df)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")
    else:
        messagebox.showinfo("Cancelado", "No se seleccionó ningún archivo.")

# Crear ventana principal
root = tk.Tk()
root.title("Análisis de CSV con Pandas")
root.geometry("600x400")

# Botón para cargar archivo
btn_cargar = tk.Button(root, text="Cargar archivo CSV", command=cargar_csv)
btn_cargar.pack(pady=10)

# Área de texto para mostrar resultados
resultado_text = scrolledtext.ScrolledText(root, width=70, height=20)
resultado_text.pack(padx=10, pady=10)

# Iniciar bucle principal
root.mainloop()
