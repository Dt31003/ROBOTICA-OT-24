from pyrplidar import PyRPlidar
import time

lidar = PyRPlidar()
lidar.connect(port="/dev/ttyUSB0", baudrate=115200, timeout=3)
# Linux   : "/dev/ttyUSB0"
# MacOS   : "/dev/cu.SLAB_USBtoUART"
# Windows : "COM5"

lidar.set_motor_pwm(500)
time.sleep(2)

scan_generator = lidar.start_scan()
    
for count, scan in enumerate(scan_generator()):
    print(count, scan)
    if count == 20: break

lidar.stop()
lidar.set_motor_pwm(0)

    
lidar.disconnect()