from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd

class LogisticRegressionModel:
    def __init__(self):
        self.data = []
        self.labels = []
        self.model = LogisticRegression(solver='liblinear')

    def agregar_datos(self, x, y, label):
        self.data.append([x, y])
        self.labels.append(label)

    def entrenar_modelo(self):
        if len(self.data) < 2:
            raise ValueError("Se requieren al menos 2 datos para entrenar.")
        X = np.array(self.data)
        y = np.array(self.labels)
        self.model.fit(X, y)

    def predecir_etiqueta(self, x, y):
        return self.model.predict([[x, y]])[0]

    def obtener_dataframe(self):
        df = pd.DataFrame(self.data, columns=["Saldo", "Movimientos"])
        df['Etiqueta'] = self.labels
        return df

    def exportar_csv(self, filename="resultados_logreg.csv"):
        df = self.obtener_dataframe()
        df.to_csv(filename, index=False)

    def resetear_datos(self):
        self.data.clear()
        self.labels.clear()
