"""INTERFACE FUNCTIONS FOR USBENCODERTEST

Mode 0 - Move toggle back and forth
Mode 1 - Virtual spring
Mode 2 - Virtual Damper
Mode 3 - Virtual Texture: Stick
Mode 4 - Virtual Texture: Slip
Mode 5 - Virtual Wall


"""


from usbencodertest import usbencodertest
import time
import cv2


MOTOR_SLEEP_TIME = 0.000001 # Amount of time to wait after writing to motor
SLOW_MOTOR_SPEED = 20

forward_direction = 1
reverse_direction = -1

DELTA_ANGLE_THRESH = 0.5

BASE_MOTOR_SPEED = 20

""" Direction key:

Angle+ is turning clockwise ("forward")
Angle- is turning counter-clockwise ("backwards")
Angle limits of paddle (if centered on zero) is -800 to 800

Direction =  0 - stopped
Direction =  1 - forward
Direction = -1 - backward

intended_direction = direction we want to be moving
motor_direction = direction the motor is currently moving
direction = angular direction we are currently moving

motor_direction and direction are different in that with user turning, the angular direction 
	we are moving could be different from the direction the motor is turning. 

"""


class user_functions:
	def __init__(self):
		""" Initializing class variables
		"""
		self.joystick = usbencodertest()
		self.clear_motor()
		self.mode = 0
		self.min_angle = -800
		self.max_angle = 800
		self.direction = 0
		self.motor_direction = 0
		self.intended_direction = 0
		self.motor_speed = 0
		self.del_angle = 0
		self.joystick.delta_angle = 0
		self.on_wall = False

	def update_vals(self):
		""" Should be called each cycle. Updates class variables with new values. 
		"""
		self.angle = self.joystick.track_angle()
		self.del_angle = self.joystick.delta_angle
		if self.del_angle > DELTA_ANGLE_THRESH:
			self.direction = -1
		elif self.del_angle < -DELTA_ANGLE_THRESH:
			self.direction = 1
		else:
			self.direction = 0
		self.a0 = self.joystick.read_a0()

	def write_motor(self,forward,backward):
		""" Writes the set duty cycle to the motor. This function should not be directly used, 
				instead use write_forward, write_backward, or clear_motor as needed. 
		"""
		self.joystick.set_duty(forward)
		self.joystick.set_duty_rev(backward)
		self.curr_drive = [forward,backward]
		#time.sleep(MOTOR_SLEEP_TIME)

	def write_forward(self,val):
		""" Writes the set duty cycle to the motor in the forward direction. Val should be between 0-100. 
		"""
		if (self.motor_direction == 1):
			# If we are already moving forward, there is no need to clear the motors. 
			pass
		elif (self.motor_direction == -1):
			self.clear_motor()
		self.write_motor(val,0)
		self.motor_direction = 1 # Update the direction
		self.motor_speed = val

	def write_backward(self,val):
		""" Writes the set duty cycle to the motor in the reverse direction. Val should be between 0-100. 
		"""
		if (self.motor_direction == -1):
			# If we are already moving backward, there is no need to clear the motor. 
			pass
		elif (self.motor_direction == 1):
			self.clear_motor()
		self.write_motor(0,val)
		self.motor_direction = -1 # Update the direction
		self.motor_speed = val

	def clear_motor(self):
		""" Clear the motor by writing zero to both directions. 
		"""
		self.write_motor(0,0)
		self.motor_direction = 0
		self.motor_speed = 0

	def run_0(self):
		""" Run program 0: move the paddle back and forth to its edges. 
		"""
		if (self.intended_direction == 1):
			if self.angle > self.max_angle:
				self.intended_direction = -1
				self.write_backward(SLOW_MOTOR_SPEED)
				print 1
			else:
				self.write_forward(SLOW_MOTOR_SPEED)
				print 2
		else:
			if self.angle < self.min_angle:
				self.intended_direction = 1
				self.write_forward(SLOW_MOTOR_SPEED)
				print 3
			else:
				self.write_backward(SLOW_MOTOR_SPEED)
				print 4

	def run_1(self):
		""" Run program 1: move the paddle in the virtual spring configuration. 
		"""
		MOTOR_SPEED = 0
		while True:
			self.update_vals()
			MOTOR_SPEED = 0.0323*self.angle - 15.806
			if (self.direction == 1):
				self.write_backward(MOTOR_SPEED)
				print 1
			elif (self.direction == -1):
				self.write_forward(MOTOR_SPEED)
				print 2

	def run_2(self):
		""" Run program 2: move the paddle in the virtual damper configuration. 
		"""
		motor_speed = BASE_MOTOR_SPEED 
		if (self.direction == 1):
			self.write_backward(motor_speed)
			print ("direction: %d, motor_direction: %d, delta_angle: %f" % (self.direction,self.motor_direction,self.del_angle))
			print 1
		elif (self.direction == -1):
			self.write_forward(motor_speed)
			print ("direction: %d, motor_direction: %d, delta_angle: %f" % (self.direction,self.motor_direction,self.del_angle))
			print 2

	def run_3(self):
		""" Run program 3: move the paddle in a slip configuration. 
		"""
		motor_speed = BASE_MOTOR_SPEED 
		if (self.direction == -1):
			self.write_backward(motor_speed)
			print ("direction: %d, motor_direction: %d, delta_angle: %f" % (self.direction,self.motor_direction,self.del_angle))
		elif (self.direction == 1):
			self.write_forward(motor_speed)
			print ("direction: %d, motor_direction: %d, delta_angle: %f" % (self.direction,self.motor_direction,self.del_angle))

	def run_4(self):
		""" Run program 4: move the paddle in a stick configuration. 
		"""
		motor_speed = BASE_MOTOR_SPEED 
		if (self.direction == 1):
			self.write_backward(motor_speed)
			print ("direction: %d, motor_direction: %d, delta_angle: %f" % (self.direction,self.motor_direction,self.del_angle))
		elif (self.direction == -1):
			self.write_forward(motor_speed)
			print ("direction: %d, motor_direction: %d, delta_angle: %f" % (self.direction,self.motor_direction,self.del_angle))


	def run_5(self, left_thresh = self.min_angle + 100, right_thresh = self.max_angle - 100):
		""" Run program 5: wall configuration. 
		"""
		if left_thresh < self.angle < right_thresh:
			if self.on_wall:
				self.clear_motor()
				self.on_wall = False
		elif self.angle < left_thresh:
			self.write_forward(100)
			self.on_wall = True
		elif self.angle > right_thresh:
			self.write_backward(100)
			self.on_wall = True


	def run_cycle(self,mode, input_val_1 = None, input_val_2 = None):
		""" Run a single cycle in the selected mode."""
		self.update_vals()
		try:
			if (mode == 0):
				self.run_0()
			elif (mode == 1):
				self.run_1()
			elif (mode == 2):
				self.run_2()
			elif (mode == 3):
				pass
				#self.run_3()
			elif (mode == 4):
				pass
				#self.run_4()
			elif (mode == 5):
				self.run_5(input_val_1,input_val_2)
		except KeyboardInterrupt:
			self.clear_motor()
			break

	def run(self):
		while True:
			self.run_cycle(2)
		#self.clear_motor()
		#self.write_forward(SLOW_MOTOR_SPEED)
		# try:
		# 	input("clear?")
		# except:
		# 	pass
		# self.clear_motor()
		# while True:
		# 	self.update_vals()
		# 	if self.mode == 0:
		# 		self.run_0()
		# 	elif self.mode == 1:
		# 		self.run_1()
		# 	elif self.mode == 2:
		# 		self.run_2()
		# 	elif self.mode == 3:
		# 		self.run_3()



if __name__ == '__main__':
	joystick = user_functions()
	joystick.run()
