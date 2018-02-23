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


class user_functions:
	def __init__(self):
		self.joystick = usbencodertest()
		self.mode = 0
		self.min_angle = -800 
		self.max_angle = 800
		self.clear_motor()
		self.direction = 0
		self.motor_direction = 0
		self.motor_speed = 0
		self.del_angle = 0
		self.joystick.delta_angle = 0
		self.intended_direction = 0

	def update_vals(self):
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
		self.joystick.set_duty(forward)
		self.joystick.set_duty_rev(backward)
		self.curr_drive = [forward,backward]
		time.sleep(MOTOR_SLEEP_TIME)

	def write_forward(self,val):
		if (self.motor_direction == 1):
			pass
		elif (self.motor_direction == -1):
			self.clear_motor()
		self.write_motor(val,0)
		self.motor_direction = 1
		self.motor_speed = val

	def write_backward(self,val):
		if (self.motor_direction == -1):
			pass
		elif (self.motor_direction == 1):
			self.clear_motor()
		self.write_motor(0,val)
		self.motor_direction = -1
		self.motor_speed = val

	def clear_motor(self):
		self.write_motor(0,0)
		self.motor_direction = 0
		self.motor_speed = 0

	def run_0(self):
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

	def run_2(self):
		motor_speed = BASE_MOTOR_SPEED + (self.del_angle*10)
		if (self.direction == 1):
			self.write_backward(motor_speed)
			print ("direction: %d, motor_direction: %d, delta_angle: %f" % (self.direction,self.motor_direction,self.del_angle))
			print 1
		elif (self.direction == -1):
			self.write_forward(motor_speed)
			print ("direction: %d, motor_direction: %d, delta_angle: %f" % (self.direction,self.motor_direction,self.del_angle))
			print 2


	def run_cycle(self,mode):
		self.update_vals()
		try:
			if (mode == 0):
				self.run_0()
			elif (mode == 1):
				pass
				#self.run_1()
			elif (mode == 2):
				self.run_2()
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
