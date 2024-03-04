from servo_control import *
from legs import *
import numpy as np
import time
from Brush import Brush


# Each of the steps is made up of 1..4 leg movements, where the t1, .. 14 steps are the movement of the legs to the specified angles.
# The multiprocessing module allows for simultanious* execution of code, you use it by initializing the tasks with:
# 'NameOfTask' = multiprocessing.Progress(target='YourFunctionName', args=('YourInputs'))
# Then starting them with:
# 'NameOfTask'.start()
# Merging them back into the stream of tasks to be done (executing and finishing):
# 'NameOfTask'.join()

def first(): # (90, 0), (90, 0), (90, 0), (90, 0)
    # 1
    t1 = multiprocessing.Process(target=north.leg_to_angles, args=(90, 0))
    t2 = multiprocessing.Process(target=east.leg_to_angles, args=(90, 0))
    t3 = multiprocessing.Process(target=west.leg_to_angles, args=(90, 0))   
    t4 = multiprocessing.Process(target=south.leg_to_angles, args=(90, 0))
    
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    
    t1.join()
    t2.join()
    t3.join()
    t4.join()

def second(): # (90, 0), (45, 45), (45, 45), (90, 0)
    # 2
    t2 = multiprocessing.Process(target=east.leg_to_angles, args=(45, 45))#down
    t3 = multiprocessing.Process(target=west.leg_to_angles, args=(45, 45))#down    
    
    t2.start()
    t3.start()
    
    t2.join()
    t3.join()

def third(): # (120, 60), (45, 45), (45, 45), (120, 0)
    # 2
    t1 = multiprocessing.Process(target=north.leg_to_angles, args=(120, 60)) # extended , but leg is down
    t4 = multiprocessing.Process(target=south.leg_to_angles, args=(120, 0)) # in, but leg is down
    
    t1.start()
    t4.start()
    
    t1.join()
    t4.join()

def fourth(): # (120, 60), (90, 0), (90, 0), (120, 0)
    # 2
    t2 = multiprocessing.Process(target=east.leg_to_angles, args=(90, 0)) #neutral
    t3 = multiprocessing.Process(target=west.leg_to_angles, args=(90, 0)) #neutral

    t2.start()
    t3.start()

    t2.join()
    t3.join()

def fifth(): # (120, 0), (90, 0), (90, 0), (120, 60)
    # 2
    t1 = multiprocessing.Process(target=north.leg_to_angles, args=(120, 0)) # in, but leg is down
    t4 = multiprocessing.Process(target=south.leg_to_angles, args=(120, 60)) # extended, but leg is down
    
    t1.start()
    t4.start()
    
    t1.join()
    t4.join()
    
    
def sixth(): # (120, 0), (90, 0), (90, 0), (120, 60)
    # 3
    t2 = multiprocessing.Process(target=east.leg_to_angles, args=(90, 0))#down
    t3 = multiprocessing.Process(target=west.leg_to_angles, args=(90, 0))#down    
    
    t2.start()
    t3.start()
    
    t2.join()
    t3.join()

def seventh(): # (45, 45), (90, 0), (90, 0), (45, 45)
    # 4
    t2 = multiprocessing.Process(target=north.leg_to_angles, args=(45, 45))#neutral
    t3 = multiprocessing.Process(target=south.leg_to_angles, args=(45, 45))#neutral 
    
    t2.start()
    t3.start()
    
    t2.join()
    t3.join()


# This is pretty hard coded right now, the inverse kinematics approach is very difficult with the inconsistent hardware,
# (meaning that the real location will not be found if you apply the formulas)
# I recommend finding the best angles by using a state space search based on some criterion of strain of the legs, 
# possibly using a genetic algorirthm.

def step(num_steps):
    # (1) north : down,    east : down,       west : down,    south : down
    # (2) north : down,    east : up(r),      west : up(r),   south : down
    # (3) north : extend,  east : up(r),      west : up(r),   south : in
    # (4) north : in,      east : up(r),      west : up(r),   south : extend
    # (5) north : in,      east : down,       west : down,    south : extend
    # (6) north : in,      east : down,       west : down,    south : extend
    # (7) north : up(r),   east : down,       west : down,    south : up(r)

    for i in range(num_steps):
        first()     # (90, 0), (90, 0), (90, 0), (90, 0)
        second()  # (90, 0), (45, 45), (45, 45), (90, 0)
        third()  # (120, 60), (45, 45), (45, 45), (120, 0)
        fourth()  # (120, 0), (45, 45), (45, 45), (120, 60)
        fifth()  # (120, 0), (90, 0), (90, 0), (120, 60)
        sixth()     # (120, 0), (90, 0), (90, 0), (120, 60)
        seventh()    # (45, 45), (90, 0), (90, 0), (45, 45)

if __name__ == '__main__':
    init()
    brush = Brush(15, 2)
    north = Leg([0, 1])   #North
    east = Leg([2, 3])   #East
    south = Leg([4, 5])   #South
    west = Leg([6, 7])   #West    
    
    brush.rotate()
    step(1) # defines how many iterations the robot's stepping function should run.
