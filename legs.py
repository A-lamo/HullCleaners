from servo_control import *
import multiprocessing
from FLCM import *
import math

class Leg:
    def __init__(self, servos):
        self.smoothness = 1
        
        self.base_servo = servos[0]
        self.top_servo = servos[1]
        
        self.base_length = 5 # placeholder, please measure
        self.top_length = 5 # placeholder, please measure
        
        self.base_angle = self.get_base_angle()
        self.top_angle = self.get_top_angle()
        self.position = self.get_position()

    def get_base_angle(self): 
        self.base_angle = pca.servo[self.base_servo].angle
        return self.base_angle
        
    def get_top_angle(self):
        self.top_angle = pca.servo[self.top_servo].angle        
        return self.top_angle

    
    # calculates the position of the tip of the leg using kinematics, the angles of the servos attached to said leg.
    def get_position(self):
        self.x = self.base_length * math.sin(self.base_angle) + self.top_length * math.cos(math.pi - self.top_angle - self.base_angle)
        self.y = self.base_length * math.cos(self.base_angle) + self.top_length * math.sin(math.pi - self.top_angle - self.base_angle) 
        self.position = (self.x, self.y)
        return self.position

    
    def leg_to_angles_test(self, bottom, top):
        self.base_angle = self.get_base_angle()
        self.top_angle = self.get_top_angle()
            
        initial_base_angle = round(self.base_angle)
        initial_top_angle = round(self.top_angle)
        
        print("INITIAL BASE ANGLE : ", initial_base_angle)
        print("INITIAL TOP ANGLE : ", initial_top_angle)
        
        bottom_distance = abs(initial_base_angle - bottom)
        top_distance = abs(initial_top_angle - top)
        
        if bottom_distance != 0 and top_distance != 0 and bottom_distance > top_distance:    
                flcm = FLCM([bottom_distance, top_distance])
                
                
                if bottom_distance < top_distance:
                    bottom_smoothness = flcm[1]*self.smoothness
                    top_smoothness = flcm[0]*self.smoothness    
                
                else:
                    bottom_smoothness = flcm[1]*self.smoothness
                    top_smoothness = flcm[0]*self.smoothness  
                    
        elif bottom_distance != 0 and top_distance != 0 and bottom_distance <= top_distance: 
                flcm = FLCM([top_distance, bottom_distance])
                
                
                if bottom_distance < top_distance:
                    bottom_smoothness = flcm[0]*self.smoothness
                    top_smoothness = flcm[1]*self.smoothness    
                
                else:
                    bottom_smoothness = flcm[0]*self.smoothness
                    top_smoothness = flcm[1]*self.smoothness  
        else:
                bottom_smoothness = self.smoothness
                top_smoothness = self.smoothness
        
        t1 = multiprocessing.Process(target=individual_servo_to_angle, args=(self.base_servo, bottom, bottom_smoothness), daemon=True)
        t2 = multiprocessing.Process(target=individual_servo_to_angle, args=(self.top_servo, top, top_smoothness), daemon=True)
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
        print(self.position)

    # Most important function of the file, that controls the two servo motors attached to a single leg simultaniously.
    # This function only works properly if the servos have been initialized, i.e. given a concrete angle before this function is executed.
    def leg_to_angles(self, bottom, top):
        
        t1 = multiprocessing.Process(target=individual_servo_to_angle, args=(self.base_servo, bottom, self.smoothness), daemon=True)
        t2 = multiprocessing.Process(target=individual_servo_to_angle, args=(self.top_servo, top, self.smoothness), daemon=True)
        
        t1.start()
        t2.start()
        
        t1.join()
        t2.join()
