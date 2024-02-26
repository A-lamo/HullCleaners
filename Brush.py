from servo_control import brushing

# This class exists currently just to create a clear difference between the leg and the brush 
# (currently both are controlled by servo motors) 
# The brush should actually be controlled by a DC motor, please implement this.
class Brush():
	def __init__(self, servo, speed):
		self.servo = servo
		self.speed = speed
		
	def rotate(self):
		brushing(self.servo, self.speed)
