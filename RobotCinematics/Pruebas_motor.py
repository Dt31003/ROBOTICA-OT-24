#>
#sudo pigpiod
from gpiozero import LED, PWMLED, AngularServo, Servo
from adafruit_servokit import ServoKit
from time import sleep
import pygame 
import numpy as np
import sys
import cv2 as cv
import math
from numpy import linalg as LA

def compute_moments(frame,):
    frame_gray = frame
    ret, thresh = cv.threshold(frame_gray, 43, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    i = 0
    for c in contours:
        # Calculate moments for each contour
        M = cv.moments(c)
            
            # Check if the moment m00 is zero to avoid division by zero
        if M["m00"] != 0:
                
                # Calculate the center of mass (centroid)
                
            if M["m10"]/10000  > 250 and M["m10"]/10000 < 600:
                mu20 = float(M["m20"] - (M["m10"]**2 /M["m00"]))
                mu02 = float(M["m02"] - (M["m01"]**2 /M["m00"]))
                mu11 = float(M["m11"] - (M["m10"]*M["m01"]/M["m00"]))
                J = np.matrix([[mu20, mu11],[mu11, mu02]])
                eigenvalues, eigenvectors = LA.eig(J)
                if eigenvalues[0] > eigenvalues[1]:
                    angle = np.degrees(math.atan2(eigenvectors[0,0],eigenvectors[0,1]))
                else: 
                    angle = np.degrees(math.atan2(eigenvectors[1,0],eigenvectors[1,1]))
                if angle > 90:
                    print("Turn to your left")
                elif angle<0:
                    print("Drop Off")
                else:
                    print("Turn to your right")
            else:
                # Handle the case where the contour has zero area (e.g., skip or set default coordinates)
                continue


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
    EN1.value = 0.5
    IN1.off()
    IN2.on()
    IN3.off()
    IN4.on()
    EN2.value = 0.5

def derecha():
    "Set the motor speed using PWM."
    EN1.value = 0.0
    EN2.value = 0.6

def izquierda():
    "Set the motor speed using PWM."
    EN1.value = 0.6
    EN2.value = 0.0

def open_camera():
    cap = cv.VideoCapture(-1)
    return cap

def inicializar_gripper(motors:ServoKit):
    motors.servo[3].angle = 90 #gripper
    motors.servo[2].angle = 80 #muneca
    motors.servo[1].angle = 50# codo
    motors.servo[0].angle = 180 #hombro
    motors.servo[15].angle = 180 #camara horizontal
    motors.servo[14].angle = 0 #camara vertical 

def cerrar_gripper(motors:ServoKit):
    motors.servo[3].angle = 90 #gripper
    sleep(1/2)
    motors.servo[2].angle = 80 #muneca
    sleep(1/2)
    motors.servo[1].angle = 50# codo
    sleep(1/2)
    motors.servo[0].angle = 180 #hombro
    sleep(1/2)
    motors.servo[15].angle = 180 #camara horizontal
    sleep(1/2)
    motors.servo[14].angle = 0 #camara vertical

def gripper(motors:ServoKit,angulo:int,i:int)->None:
    motors.servo[i].angle = angulo
    
def actualizarangulo(angulo:int,actualizacion:int,i:int)->int:
    angulo += actualizacion 
    if i == 3:
        angulo = max(30,min(180,angulo))
    else:
        angulo = max(0,min(180,angulo))        
    sleep(0.005)
    return angulo
    

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
    angulo1 = 180 
    angulo2 = 50
    angulo3 = 80
    angulo4 = 90
    angulo_horizontal = 180
    angulo_vertical = 0
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
            angulo1 = actualizarangulo(angulo1,1,0)
            gripper(kit,angulo1,0)
        if keys[pygame.K_h]:
            angulo1 = actualizarangulo(angulo1,-1,0)
            gripper(kit,angulo1,0)
        if keys[pygame.K_u]:
            angulo2 = actualizarangulo(angulo2,1,1)
            gripper(kit,angulo2,1)
        if keys[pygame.K_j]:
            angulo2 = actualizarangulo(angulo2,-1,1)
            gripper(kit,angulo2,1)
        if keys[pygame.K_i]:
            angulo3 = actualizarangulo(angulo3,1,2)
            gripper(kit,angulo3,2)
        if keys[pygame.K_k]:
            angulo3 = actualizarangulo(angulo3,-1,2)
            gripper(kit,angulo3,2)
        if keys[pygame.K_o]:
            angulo4 = actualizarangulo(angulo4,1,3)
            gripper(kit,angulo4,3)
        if keys[pygame.K_l]:
            angulo4 = 30
            gripper(kit,angulo4,3)  
        if keys[pygame.K_r]: #Angulo horizontal
            angulo_horizontal = actualizarangulo(angulo_horizontal,1,15)
            gripper(kit,angulo_horizontal,15)
        if keys[pygame.K_f]: #Angulo horizontal
            angulo_horizontal = actualizarangulo(angulo_horizontal,-1,15)
            gripper(kit,angulo_horizontal,15)
        if keys[pygame.K_t]:
            angulo_vertical = actualizarangulo(angulo_vertical,1,14)
            gripper(kit,angulo_vertical,14)
        if keys[pygame.K_g]:
            angulo_vertical = actualizarangulo(angulo_vertical,-1,14)
            gripper(kit,angulo_vertical,14)
        if keys[pygame.K_c] and control:
            compute_moments(frame)
        if control:
            ret, frame = cap.read()
            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            if ret:
                cv.imshow('Camera',frame)
                cv.waitKey(1)
        control_screen.fill('black')
        pygame.display.flip()
        
    cerrar_gripper(kit)
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