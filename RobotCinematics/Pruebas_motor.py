from gpiozero import LED, PWMLED
from time import sleep
import pygame 
import numpy as np
import sys
import cv2

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

    

if __name__ == "__main__":
    pygame.init()
    control_screen = pygame.display.set_mode((240,180))
    pygame.display.set_caption('control devices')
    run = True
    value = 0.0
    IN1 = LED(17) 
    IN2 = LED(27)
    EN1 = PWMLED(13, active_high=True, initial_value=0)
    IN3 = LED(1) 
    IN4 = LED(7)
    EN2 = PWMLED(12, active_high=True, initial_value=0)
    
    speed_values = {
        pygame.K_0: 0.0,
        pygame.K_1: 0.2,
        pygame.K_2: 0.4,
        pygame.K_3: 0.6,
        pygame.K_4: 0.8,
        pygame.K_5: 1.0
    }
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
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
            run = False
        if keys[pygame.K_LEFT]:
            izquierda()
        if keys[pygame.K_RIGHT]:
            derecha()
        control_screen.fill('black')
        pygame.display.flip()
    pygame.quit()
    print("Finishing program")
    EN1.value = 0.0
    IN1.off()
    IN2.off()
    EN2.value = 0.0
    IN3.off()
    IN4.off() 
    sys.exit()      