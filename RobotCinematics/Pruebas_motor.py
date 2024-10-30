#>
#sudo pigpiod
from gpiozero import LED, PWMLED, AngularServo, Servo
from adafruit_servokit import ServoKit
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import pygame 
import numpy as np
import sys
import cv2 as cv
import math

def set_speed(value):
    "Set the motor speed using PWM."
    EN1.value = value
    IN1.on()
    IN2.off()
    IN3.on()
    IN4.off()
    EN2.value = value

def reversa():
    "Set the motor speed using PWM."
    EN1.value = 0.7
    IN1.off()
    IN2.on()
    IN3.off()
    IN4.on()
    EN2.value = 0.5

def derecha():
    "Set the motor speed using PWM."
    EN1.value = 0.2
    EN2.value = 0.6

def izquierda():
    "Set the motor speed using PWM."
    EN1.value = 0.6
    EN2.value = 0.2

def open_camera():
    cap = cv.VideoCapture(0)
    return cap

def inicializar_gripper(motors:ServoKit):
    for i in range(0,4):
        motors.servo[i].angle = 0

def gripper(motors:ServoKit,angulo:int,i:int)->None:
    motors.servo[i].angle = angulo
    
def actualizarangulo(angulo:int,actualizacion:int)->int:
    angulo += 3*actualizacion 
    sleep(0.005)
    return max(0, min(180, angulo))
    
def actualiar_camara(condicion:bool, camara:ServoKit):
    if condicion == True:
        camara.servo[4].angle = 180
    else:
        camara.servo[4].angle = 0
    sleep(2/1000)
if __name__ == "__main__":
    pygame.init()
    control_screen = pygame.display.set_mode((240,180))
    pygame.display.set_caption('control devices')
    run = True
    camara= False #variable de control de orientacion de la camara,inicia adelante
    value = 0.0 #valor de velocidad del carro
    #motores
    IN1 = LED(17) 
    IN2 = LED(27)
    EN1 = PWMLED(13, active_high=True, initial_value=0)
    IN3 = LED(1) 
    IN4 = LED(7)
    EN2 = PWMLED(12, active_high=True, initial_value=0)
    #servos
    kit = ServoKit(channels=16)
    inicializar_gripper(kit)
    #angulos de los servos
    angulo1 = 0 
    angulo2 = 0
    angulo3 = 0
    angulo4 = 0
    #funcion de velocidades
    speed_values = {
        pygame.K_0: 0.0,
        pygame.K_1: 0.2,
        pygame.K_2: 0.4,
        pygame.K_3: 0.6,
        pygame.K_4: 0.8,
        pygame.K_5: 1.0
    }
    cap = open_camera()
    control = cap.isOpened() #Despliega o no la camara
    if not control:
        print("No se detecto una camara")
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                #si se dejan de presionar las teclas el motor dejara de avanzar
                if event.key in speed_values:
                    value = speed_values[event.key]
            elif event.type == pygame.KEYUP:
                set_speed(0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            set_speed(value)
        elif keys[pygame.K_DOWN]:
            reversa()
        elif keys[pygame.K_e]:
            set_speed(0.0)
        elif keys[pygame.K_a]:
            #sale del bucle
            run = False
        if keys[pygame.K_LEFT]:
            izquierda()
        if keys[pygame.K_RIGHT]:
            derecha()
        if keys[pygame.K_y]:
            angulo1 = actualizarangulo(angulo1,1)
            gripper(kit,angulo1,0)
        if keys[pygame.K_h]:
            angulo1 = actualizarangulo(angulo1,-1)
            gripper(kit,angulo1,0)
        if keys[pygame.K_u]:
            angulo2 = actualizarangulo(angulo2,1)
            gripper(kit,angulo2,1)
        if keys[pygame.K_j]:
            angulo2 = actualizarangulo(angulo2,-1)
            gripper(kit,angulo2,1)
        if keys[pygame.K_i]:
            angulo3 = actualizarangulo(angulo3,1)
            gripper(kit,angulo3,2)
        if keys[pygame.K_k]:
            angulo3 = actualizarangulo(angulo3,-1)
            gripper(kit,angulo3,2)
        if keys[pygame.K_o]:
            angulo4 = actualizarangulo(angulo4,1)
            gripper(kit,angulo4,3)
        if keys[pygame.K_l]:
            angulo4 = actualizarangulo(angulo4,-1)
            gripper(kit,angulo4,3)  
        if keys[pygame.K_SPACE]:
            camara = not camara
            actualiar_camara(camara,kit)
        if control:
            ret, frame = cap.read()
            if ret:
                frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
                cv.imshow('Camera',frame)
                cv.waitKey(1)
        print(angulo1)
        control_screen.fill('black')
        pygame.display.flip()
        
        
    cv.destroyAllWindows()   
    cap.release()
    pygame.quit()
    print("Finishing program")
    EN1.value = 0.0
    IN1.off()
    IN2.off()
    EN2.value = 0.0
    IN3.off()
    IN4.off() 
    sys.exit()     