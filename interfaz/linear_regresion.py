import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Leer el archivo CSV real
df = pd.read_csv('test.csv')  # Asegúrate de que el archivo esté en la misma carpeta
#Limpieza de datos
df = df.dropna()

# Seleccionar las características y la variable objetivo
X = df[['x']]
y = df['y']

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Hacer predicciones
y_pred = model.predict(X_test)

# Evaluar el modelo
mse = mean_squared_error(y_test, y_pred)
print(f'Error Cuadrático Medio: {mse:.4f}')

# Graficar resultados
plt.scatter(X_test, y_test, color='blue', label='Datos Reales')
plt.plot(X_test, y_pred, color='red', linewidth=2, label='Predicción')
plt.xlabel('Horas de estudio (x)')
plt.ylabel('Puntuación de examen (y)')
plt.title('Regresión Lineal: x vs y')
plt.legend()
plt.grid()
plt.show()
