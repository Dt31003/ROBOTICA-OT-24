from rplidar import RPLidar
import numpy as np
import matplotlib.pyplot as plt
import time
# Par�metros de configuraci�n
DEVICE_PATH = '/dev/ttyUSB0'  # Cambia esto seg�n tu puerto
BAUD_RATE = 115200
TIMEOUT = 1

D_MAX = 6000  # Distancia m�xima que se muestra en el gr�fico (mm)

# Iniciar RPLidar
lidar = RPLidar(port=DEVICE_PATH, baudrate=BAUD_RATE, timeout=TIMEOUT)
lidar.start_motor()
time.sleep(2)
# Tomar un solo escaneo
try:
    
    # Primera iteracion
    scan = next(lidar.iter_scans(max_buf_meas=8000))  # Obtener el segundo escaneo
    time.sleep(2)
    scan = next(lidar.iter_scans(max_buf_meas=8000))  # Obtener el segundo escaneo    
    # Convertir los datos a un formato adecuado
    angles = [np.radians(meas[1]) for meas in scan]  # Convertir angulos a radianes
    distances = [meas[2] for meas in scan]  # Obtener las distancias
    
    # -------------------------------
    # Graficar en coordenadas polares
    # -------------------------------
    plt.figure(figsize=(12, 6))

    # Crear la figura para el grafico polar
    ax1 = plt.subplot(111, projection='polar')
    ax1.set_title("Escaneo LIDAR - Polar")
    ax1.set_rmax(D_MAX)
    ax1.grid(True)

    # Crear el grafico polar
    ax1.scatter(angles, distances, c=distances, cmap='plasma', s=10, lw=0, alpha=0.75)

    # -------------------------------
    # Graficar en coordenadas cartesianas
    # -------------------------------
    plt.figure(figsize=(6, 6))

    # Crear la figura para el grafico cartesiano
    ax2 = plt.subplot(111)
    ax2.set_title("Escaneo LIDAR - Cartesiano")
    ax2.set_xlim(0, 400)
    ax2.set_ylim(0, 600)
    ax2.set_aspect('equal', 'box')
    ax2.grid(True)

    # Crear el grafico cartesiano utilizando angulos en grados y distancias
    ax2.scatter(np.degrees(angles), np.array(distances)/10, c=distances, cmap='plasma', s=10, lw=0, alpha=0.75)

    plt.tight_layout()
    plt.show()

    raw_data = np.matrix[angles,distances]
    print(raw_data)

finally:
    # Detener el motor y desconectar el LIDAR
    lidar.stop_motor()
    lidar.stop()
    lidar.disconnect()
