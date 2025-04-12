import numpy as np
import matplotlib.pyplot as plt

def linear_regresion():
    # Generar datos sintéticos
    x = np.linspace(0, 10, 100)  # Características de entrada
    y = 2 * x + np.random.randn(100) * 2  # Objetivo con algo de ruido

    # Calcular los coeficientes de regresión lineal
    A = np.vstack([x, np.ones(len(x))]).T  # Matriz de diseño
    m, b = np.linalg.lstsq(A, y, rcond=None)[0]  # Resolver para m (pendiente) y b (intercepto)

    # Graficar los puntos de datos y la línea de regresión
    plt.scatter(x, y, color='blue', label='Puntos de Datos')  # Gráfico de dispersión para los puntos de datos
    plt.plot(x, m * x + b, color='red', label='Línea de Regresión')  # Línea para la regresión lineal
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.title('Regresión Lineal usando NumPy y Matplotlib')
    plt.legend()
    plt.show()

# Llamar a la función para ejecutar la regresión lineal
linear_regresion()
