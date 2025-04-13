import tkinter as tk
from tkinter import messagebox
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
import pandas as pd

#Clustering

class ClusteringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clustering Demo")
        self.root.geometry("250x300")

        self.data = []

        coord_frame = tk.Frame(root, bg="#FFFFFF", padx=10, pady=10)
        coord_frame.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(coord_frame, text="Saldo:", bg="#FFFFFF").grid(row=0, column=0)
        self.x_entry = tk.Entry(coord_frame)
        self.x_entry.grid(row=0, column=1)

        tk.Label(coord_frame, text="Movimientos:", bg="#FFFFFF").grid(row=1, column=0)
        self.y_entry = tk.Entry(coord_frame)
        self.y_entry.grid(row=1, column=1)

        tk.Button(coord_frame, text="Agregar Datos", command=self.agregar_datos).grid(row=2, column=0, columnspan=2,
                                                                                      pady=5)

        tk.Label(root, text="Número de Clusters:").grid(row=1, column=0)
        self.k_entry = tk.Entry(root)
        self.k_entry.grid(row=1, column=1)

        tk.Button(root, text="Realizar Clustering", command=self.hacer_clustering).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Ver lista de datos", command=self.mostrar_dataframe).grid(row=3, column=0, columnspan=2, pady=5)

    def agregar_datos(self):
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
            self.data.append([x, y])
            self.x_entry.delete(0, tk.END)
            self.y_entry.delete(0, tk.END)
            messagebox.showinfo("Datos agregados", f"Datos ({x}, {y}) agregados correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce datos numéricos.")

    def hacer_clustering(self):
        if len(self.data) < 2:
            messagebox.showerror("Error", "Debes ingresar al menos dos datos numericos.")
            return

        try:
            k = int(self.k_entry.get())
            if k <= 0 or k > len(self.data):
                raise ValueError

            #Resultado de los datos

            kmeans = KMeans(n_clusters=k)
            kmeans.fit(self.data)
            labels = kmeans.labels_
            centroids = kmeans.cluster_centers_
            inercia = kmeans.inertia_

            messagebox.showinfo("Inercia", f"Inercia del modelo: {inercia:.2f}")

            color_list = list(mcolors.TABLEAU_COLORS.values())
            random.shuffle(color_list)

            plt.figure()
            for i in range(k):
                cluster = [self.data[j] for j in range(len(self.data)) if labels[j] == i]
                x_vals = [point[0] for point in cluster]
                y_vals = [point[1] for point in cluster]
                color = color_list[i % len(color_list)]
                plt.scatter(x_vals, y_vals, color=color, label=f"Cluster {i + 1}")
                plt.scatter(centroids[i][0], centroids[i][1], s=200, c=color, marker='X', edgecolors='black')

            plt.title(f"Cuentas (Inercia: {inercia:.2f})")
            plt.xlabel("Saldo de cuentas", fontsize=15)
            plt.ylabel("Cantidad de movimientos de la tarjeta", fontsize=15)
            plt.legend()
            plt.grid(True)
            plt.show()

        except ValueError:
            messagebox.showerror("Error", "Introduce un número válido de clusters.")

    def obtener_dataframe(self):
        if not self.data:
            messagebox.showinfo("Sin datos", "No hay datos ingresados.")
            return None
        return pd.DataFrame(self.data, columns=['Saldo', 'Movimientos'])

    def mostrar_dataframe(self):
        df = self.obtener_dataframe()
        if df is not None:
            ventana = tk.Toplevel(self.root)
            ventana.title("Datos Ingresados")
            text = tk.Text(ventana, width=30, height=10)
            text.insert(tk.END, df.to_string(index=False))
            text.pack(padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClusteringApp(root)
    root.mainloop()
