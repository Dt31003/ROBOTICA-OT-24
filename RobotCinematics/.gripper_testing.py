from gpiozero import LED, PWMLED, AngularServo, Servo
from adafruit_servokit import ServoKit

motors = ServoKit(channels=16)
motors.servo[3].angle = 90 #gripper
motors.servo[2].angle = 80 #muneca
motors.servo[1].angle = 50# codo
motors.servo[0].angle = 180 #hombro

while(1):
    angulo = int(input("Angulo de giro deseado:"))
    kit.servo[0].angle = angulo
    if angulo > 180:
        break    