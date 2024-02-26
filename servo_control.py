#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Libraries
import multiprocessing
import time    #https://docs.python.org/fr/3/library/time.html
from adafruit_servokit import ServoKit    #https://circuitpython.readthedocs.io/projects/servokit/en/latest/
from FLCM import *
#Constants
nbPCAServo=16 

#Parameters
MIN_IMP = [500 for i in range(16)]
MAX_IMP = [2500 for i in range(16)]
MIN_ANG = [0 for i in range(16)]
MAX_ANG = [180 for i in range(16)]
INIT_ANG = [0 for i in range(16)]

#Objects, 
# the servo hat we use can control 16 servos at once. 
pca = ServoKit(channels=16)

# Initializes the servos to a specific angle,
# if one of them is not properly set up the functions built after this will fail.
def init():
     for i in range(nbPCAServo):
         pca.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])
     for i in range(nbPCAServo):
         pca.servo[i].angle = 0
         print(f"SERVO {i} ANGLE = ",pca.servo[i].angle)

# function to test whether the servos are working properly in tandem
# going up to their max angle, coming back to their min.
def pcaScenario():
    """Scenario to test servo"""
    for i in range(nbPCAServo):
        for j in range(MIN_ANG[i],MAX_ANG[i],1):
            print("Send angle {} to Servo {}".format(j,i))
            pca.servo[i].angle = j
            time.sleep(0.01)
        for j in range(MAX_ANG[i],MIN_ANG[i],-1):
            print("Send angle {} to Servo {}".format(j,i))
            pca.servo[i].angle = j
            time.sleep(0.01)
        pca.servo[i].angle=None #disable channel
        time.sleep(0.5)

# Sets an individual servo to a specific angle.
def individual_servo_to_angle(num, angle, phi):
    initial_angle = int(pca.servo[num].angle)
    if initial_angle < angle:
        for j in range(phi*initial_angle,phi*angle+1,1):
                print("Send angle {} to Servo {}".format(j/phi,num))
                pca.servo[num].angle = (1/phi)*j
                print(f"ACTUAL ANGLE OF SERVO {num} IS {pca.servo[num].angle}")
                time.sleep(0.01)
    else:
        
        for j in range(phi*initial_angle,phi*angle+1,-1):
            print("Send angle {} to Servo {}".format(j/phi,num))
            pca.servo[num].angle = (1/phi)*j
            print(f"ACTUAL ANGLE OF SERVO {num} IS {pca.servo[num].angle}")
            time.sleep(0.01)


# This function is not currently used, I was planning on using it to add angles incrementally,
# however for some reason setting to the value in small steps, without using addition works far better.
# TODO: figure out why...
def add_angle(num, theta, phi):
    print('CALLING FUNCTION \'add_angle()\'')

    initial_angle = pca.servo[num].angle 
    print(f"INITIAL ANGLE OF THE SERVO {num} IS {initial_angle}")
    
    if theta>0:
        step_type = 1
    else:
        step_type = -1
         
    if MIN_ANG[num] < (initial_angle + 2*theta) < MAX_ANG[num]:
        print("STARTING MOVEMENT...")
        print(f"MOVING JOINT ATTACHED TO SERVO {num} {theta} DEGREES")
        for i in range(int(phi*initial_angle), int(phi*(initial_angle + 2*theta)), step_type):
            pca.servo[num].angle = (1/phi)*i
    else:
        print("THE MOVEMENT REQUESTED IS ILLEGAL...")
    print(f"TERMINAL ANGLE OF THE SERVO {num} IS {pca.servo[num].angle}")


# Set servo to a specific angle, split in two because you can go in a negative direction as well.
def to_angle(num, initial, end, phi):
    if initial <= end:
        for i in range(initial, end*phi, 1):
            pca.servo[num].angle = i/phi
    else:
        for i in range(initial*phi, end, -1):
            pca.servo[num].angle = i/phi            

# set servo to its minimal angle
def to_min(num, phi):
    while pca.servo[num].angle > 0:
        pca.servo[num].angle -= 1/phi
        print(pca.servo[num].angle)


# Goes back and forth with the servo that is responsible for controlling the brush. 
# Again, this should be a DC motor, doing this with a servo is a temporary solution
def brushing(num, stepsize):
    while True:
        for i in range(MIN_ANG[num], MAX_ANG[num], stepsize):
            pca.servo[num].angle = i
            print("Send angle {} to Brush Servo {}".format(i,num))   
        time.sleep(0.1)
        for i in range(MAX_ANG[num], MIN_ANG[num], -stepsize):
            pca.servo[num].angle = i
            print("Send angle {} to Brush Servo {}".format(i,num))       


# largest common multiple
def lcm(a,b):
    if a > b:
        greater = a
    else:
        greater = b
        
    while True:
        if (greater % a == 0) and (greater % b == 0):
            lcm = greater
            break
        greater += 1
    return lcm

# greatest common divisor
def gcd(a, b): 
    if a == 0:
        return b
    return gcd(b % a, a)
            

#def smooth_servo_move(servo, target_angle, duration=1.0):
#    steps = 50  # Adjust the number of steps as needed
#    sleep_time = duration / steps
#    
#    if servo.angle:
#        current_angle = int(servo.angle)
#    else:
#        current_angle = 0
#    angle_step = (target_angle - current_angle) / steps
#
#    for _ in range(steps):
#        current_angle += angle_step
#        servo.angle = current_angle
#        time.sleep(sleep_time)
 
