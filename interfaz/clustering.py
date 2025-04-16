from sklearn.cluster import KMeans
import pandas as pd

class ClusteringModel:
    def __init__(self):
        self.data = []

    def agregar_datos(self, x, y):
        self.data.append([x, y])

    def hacer_clustering(self, k):
        if len(self.data) < 2:
            raise ValueError("Debes ingresar al menos dos datos numéricos.")
        if k <= 0 or k > len(self.data):
            raise ValueError("Introduce un número válido de clusters.")

        kmeans = KMeans(n_clusters=k)
        kmeans.fit(self.data)
        labels = kmeans.labels_
        centroids = kmeans.cluster_centers_
        inercia = kmeans.inertia_

        return labels, centroids, inercia

    def obtener_dataframe(self):
        if not self.data:
            return None
        return pd.DataFrame(self.data, columns=['Saldo', 'Movimientos'])
