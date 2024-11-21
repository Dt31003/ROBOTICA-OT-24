from os import path
from sys import exit
 
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import time
from rplidar import RPLidar
 
 
BAUD_RATE: int = 115200
TIMEOUT: int = 3
 
LINUX_DEVICE_PATH: str = '/dev/ttyUSB0'
DEVICE_PATH: str = LINUX_DEVICE_PATH
 
D_MAX: int = 6000   # Max lidar range
# rango de intensidades
I_MIN: int = 0
I_MAX: int = 50
 

# verifica que exista la path (conexion con lidar) 
def verify_device() -> bool:
    if path.exists(DEVICE_PATH):
        return True
    else:
        return False
 
 
# recuperacion de datos
# meas[0] = intensidad
# meas[1] = angulo
# meas[2] = distancia

def update_line(num, iterator, line):
    scan = next(iterator)
 
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intents = np.array([meas[0] for meas in scan])
    line.set_array(intents)
    
    return line
 
 
if __name__ == '__main__':
    # Busca el dispositivo
    if not verify_device():
        print(f'No device found: {DEVICE_PATH}')
        exit(1)
    
    # Conecta con el dispositivo
    lidar = RPLidar(port=DEVICE_PATH, baudrate=BAUD_RATE, timeout=TIMEOUT)
    
    # Inicializa el motor del lidar
    lidar.start_motor()
 
    try:
        plt.rcParams['toolbar'] = 'None'
        fig = plt.figure()
 
        ax = plt.subplot(111, projection='polar')
        # Fondo del plot
        line = ax.scatter([0, 0], [0, 0], s=5, c=[0, 50], cmap='plasma', lw=0)
 
        ax.set_rmax(D_MAX)
 
        ax.grid(True)
        # numero de datos
        iterator = lidar.iter_scans(max_buf_meas=8000)
        # Actualiza los puntos en tiempo real
        ani = animation.FuncAnimation(fig, update_line, fargs=(iterator, line), interval=50, cache_frame_data=False)
 
        plt.show()
 
    except KeyboardInterrupt:
        lidar.stop_motor()
        time.sleep(2)
        lidar.stop()
        
        lidar.disconnect()