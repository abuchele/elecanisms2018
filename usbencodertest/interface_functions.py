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


MOTOR_SLEEP_TIME = 0.000001 # Amount of time to wait after writing to motor
SLOW_MOTOR_SPEED = 10

forward_direction = 1
reverse_direction = -1


class user_functions:
	def __init__(self):
		self.joystick = usbencodertest()
		self.mode = 0
		self.min_angle = -800 
		self.max_angle = 800
		self.clear_motor()
		self.direction = 0

	def update_vals(self):
		self.angle = self.joystick.track_angle()
		self.del_angle = self.joystick.delta_angle
		self.a0 = self.joystick.read_a0()

	def write_motor(self,forward,backward):
		self.joystick.set_duty(forward)
		self.joystick.set_duty_rev(backward)
		self.curr_drive = [forward,backward]
		time.sleep(MOTOR_SLEEP_TIME)

	def write_forward(self,val):
		self.clear_motor()
		self.write_motor(val,0)

	def write_backward(self,val):
		self.clear_motor()
		self.write_motor(0,val)

	def clear_motor(self):
		self.write_motor(0,0)

	def run_0(self):
		intended_direction = 0
		while True:
			self.update_vals()
			if intended_direction:
				if self.angle < self.min_angle:
					if (self.direction == 1):
						intended_direction = 0
						print 0
					else:
						self.write_forward(SLOW_MOTOR_SPEED)
						self.direction = 1
						intended_direction = 0
						print 1
				else:
					if (self.direction == -1):
						self.write_backward(SLOW_MOTOR_SPEED)
						print 2
					else:
						self.write_backward(SLOW_MOTOR_SPEED)
						self.direction = -1
						print 3
			else:
				if self.angle > self.max_angle:
					if (self.direction == -1):
						intended_direction = 1
						print 4
					else:
						self.write_backward(SLOW_MOTOR_SPEED)
						self.direction = -1
						intended_direction = 1
						print 5
				else:
					if (self.direction == 1):
						print 6
						self.write_forward(SLOW_MOTOR_SPEED)
						pass
					else:
						self.write_forward(SLOW_MOTOR_SPEED)
						self.direction = 1
						print 7
			print self.angle


		


	def run(self):
		self.run_0()
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
