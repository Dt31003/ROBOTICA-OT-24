from gpiozero import LED, PWMLED
from time import sleep

def set_speed(value):
    """Set the motor speed using PWM."""
    EN1.value = value
    IN1.on()
    IN2.off()
    IN3.off()
    IN4.on()
    EN2.value = value

def reversa():
    """Set the motor speed using PWM."""
    EN1.value = 0.5
    IN1.off()
    IN2.on()
    IN3.on()
    IN4.off()
    EN2.value = 0.5

def derecha():
    """Set the motor speed using PWM."""
    EN1.value = 0.2
    IN1.on()
    IN2.off()
    IN3.off()
    IN4.on()
    EN2.value = 0.6

def izquierda():
    """Set the motor speed using PWM."""
    EN1.value = 0.6
    IN1.on()
    IN2.off()
    IN3.off()
    IN4.on()
    EN2.value = 0.2

if __name__ == "__main__":
    IN1 = LED(17)
    IN2 = LED(27)
    EN1 = PWMLED(13, active_high=True, initial_value=0)
    IN3 = LED(1)
    IN4 = LED(7)
    EN2 = PWMLED(12, active_high=True, initial_value=0)


    speed_functions = {
        1: lambda: set_speed(0.2),
        2: lambda: set_speed(0.4),
        3: lambda: set_speed(0.6),
        4: lambda: set_speed(0.8),
        5: lambda: set_speed(1.0),
    }

    try:
        while True:
            try:
                X = int(input("Ingrese la velocidad (0-5), izquierda(7), derecha(8) o 6 para salir: "))
                if X in speed_functions:
                    speed_functions[X]()
                elif X == 6:
                    break
                elif X == 0:
                    reversa()
                elif X == 7:
                    izquierda
                elif X == 8:
                    derecha()
                else:
                    print("Por favor ingrese un nÃºmero entre 1 y 6.")
            except ValueError:
                print("Entrada invÃ¡lida. Por favor ingrese un nÃºmero.")

    finally:
        print("Finishing program")
        EN1.value = 0.0
        IN1.off()
        IN2.off()   