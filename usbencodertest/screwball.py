from usbencodertest import usbencodertest
import time
import os
import random



class motor_control:
	def __init__(self):
		""" Initializing class variables
		"""
		self.joystick = usbencodertest()
		self.clear_motor()
		self.mode = -1
		self.min_angle = -800
		self.max_angle = 800
		self.direction = 0
		self.motor_direction = 0
		self.intended_direction = 0
		self.motor_speed = 0
		self.del_angle = 0
		self.joystick.delta_angle = 0
		self.on_wall = False
		self.filename = self.generate_filename(0)
		self.writefile = open(self.filename,'w')
		self.starttime = time.time()
		self.wall_loc_left = -400
		self.wall_loc_right = 400
		self.angle = 0

	def generate_filename(self,fnum):
		""" Generates a new filename to save the data. """
		xx = str(fnum)+".csv"
		if os.path.isfile(os.path.join('datafiles', xx)):
			return self.generate_filename(fnum + 1)
		return os.path.join('datafiles', xx)

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
		time.sleep(MOTOR_SLEEP_TIME)

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

	def record_angle(self):
		self.writefile.write(str('{:f}'.format(self.angle)) + ',' + str(time.time()-self.starttime) + ';')
		self.writefile.write('\n')

	def reset_angle(self):
		self.angle = 0
		self.del_angle = 0
		self.joystick.delta_angle = 0
		self.joystick.total_angle = 0

	def run_calibration(self):
		""" Prints the current angle so we can calibrate the system to be centered at angle = 0. """
		self.clear_motor()
		print self.angle

	def run_0(self):
		""" Run program 0: move the paddle back and forth to its edges. 
		"""
		if ((self.angle > self.max_angle) or (self.angle < self.min_angle)):
			self.clear_motor()
		else:
			if (self.intended_direction == 1):
				if self.angle > self.max_angle:
					self.intended_direction = -1
					self.write_backward(SLOW_MOTOR_SPEED)
				else:
					self.write_forward(SLOW_MOTOR_SPEED)
			else:
				if self.angle < self.min_angle:
					self.intended_direction = 1
					self.write_forward(SLOW_MOTOR_SPEED)
				else:
					self.write_backward(SLOW_MOTOR_SPEED)

	def run_1(self):
		""" Run program 1: move the paddle in the virtual spring configuration. 
		"""
		if ((self.angle > self.max_angle) or (self.angle < self.min_angle)):
			self.clear_motor()
		else:
			MOTOR_SPEED = abs((0.1)*abs(self.angle) + 14)
			if (self.angle > ZERO_ANGLE_THRESH):
				if MOTOR_SPEED < 15:
					self.clear_motor()
				else:
					self.write_forward(MOTOR_SPEED)
			elif (self.angle < -ZERO_ANGLE_THRESH):
				if MOTOR_SPEED < 15:
					self.clear_motor()
				else:
					self.write_backward(MOTOR_SPEED)
			else:
				self.clear_motor()

	def run_2(self):
		""" Run program 2: move the paddle in the virtual damper configuration. 
		"""
		motor_speed = BASE_MOTOR_SPEED*(self.del_angle/50)
		if ((self.angle > self.max_angle) or (self.angle < self.min_angle)):
			self.clear_motor()
		else:
			if (self.direction == 1):
				self.write_backward(motor_speed)
			elif (self.direction == -1):
				self.write_forward(motor_speed)

	def run_3(self):
		""" Run program 3: move the paddle in a slip configuration. 
		"""
		motor_speed = BASE_MOTOR_SPEED 
		if ((self.angle > self.max_angle) or (self.angle < self.min_angle)):
			self.clear_motor()
		else:
			if (self.direction == -1):
				self.write_backward(motor_speed)
			elif (self.direction == 1):
				self.write_forward(motor_speed)

	def run_4(self):
		""" Run program 4: move the paddle in a stick configuration. 
		"""
		motor_speed = BASE_MOTOR_SPEED 
		if ((self.angle > self.max_angle) or (self.angle < self.min_angle)):
			self.clear_motor()
		else:
			if (self.direction == 1):
				self.write_backward(motor_speed)
			elif (self.direction == -1):
				self.write_forward(motor_speed)


	def run_5(self, left_thresh, right_thresh):
		""" Run program 5: wall configuration. 
		"""
		if ((self.angle > self.max_angle) or (self.angle < self.min_angle)):
			self.clear_motor()
		else:
			if ((left_thresh is not None) and (right_thresh is not None)):
				left_thresh = int(left_thresh)
				right_thresh = int(right_thresh)
				if ((left_thresh < self.angle) and (self.angle < right_thresh)):
					if self.on_wall:
						self.clear_motor()
						self.on_wall = False
				elif (self.angle < left_thresh):
					self.write_backward(100)
					self.on_wall = True
					time.sleep(MOTOR_SLEEP_TIME)
				elif (self.angle > right_thresh):
					self.write_forward(100)
					self.on_wall = True
					time.sleep(MOTOR_SLEEP_TIME)
			elif (left_thresh is not None):
				if (left_thresh < self.angle):
					if self.on_wall:
						self.clear_motor()
						self.on_wall = False
					elif self.angle < left_thresh:
						self.write_backward(100)
						self.on_wall = True
						time.sleep(MOTOR_SLEEP_TIME)
			elif (right_thresh is not None):
				if (self.angle < right_thresh):
					if self.on_wall:
						self.clear_motor()
						self.on_wall = False
					elif self.angle > right_thresh:
						self.write_forward(100)
						self.on_wall = True
						time.sleep(MOTOR_SLEEP_TIME)


	def run_cycle(self, mode):
		""" Run a single cycle in the selected mode."""
		self.update_vals()
		self.record_angle()
		#self.run_5(self.wall_loc_left,self.wall_loc_right)
		try:
			if (mode == 0):
				try:
					self.run_0()
				except KeyboardInterrupt:
					self.clear_motor()
			elif (mode == 1):
				try:
					self.run_1()
				except KeyboardInterrupt:
					self.clear_motor()
			elif (mode == 2):
				try:
					self.run_2()
					time.sleep(10*MOTOR_SLEEP_TIME)
					self.clear_motor()
					time.sleep(MOTOR_SLEEP_TIME)
				except KeyboardInterrupt:
					self.clear_motor()
			elif (mode == 3):
				try:
					self.run_3()
				except KeyboardInterrupt:
					self.clear_motor()
			elif (mode == 4):
				try:
					self.run_4()
					time.sleep(4*MOTOR_SLEEP_TIME)
					self.clear_motor()
					time.sleep(2*MOTOR_SLEEP_TIME)
				except KeyboardInterrupt:
					self.clear_motor()
			elif (mode == 5):
				try:
					self.run_5(self.wall_loc_left,self.wall_loc_right)
				except KeyboardInterrupt:
					self.clear_motor()
			elif (mode == -1):
				try:
					self.run_calibration()
				except KeyboardInterrupt:
					self.clear_motor()
		except KeyboardInterrupt:
			self.clear_motor()

	def run_stick_cycle(self):
		self.run_cycle(4)
		time.sleep(4*MOTOR_SLEEP_TIME)
		self.clear_motor()
		time.sleep(2*MOTOR_SLEEP_TIME)

	def run_slip_cycle(self):
		self.run_cycle(3)
		time.sleep(4*MOTOR_SLEEP_TIME)
		self.clear_motor()
		time.sleep(MOTOR_SLEEP_TIME)

	def run_slip_and_stick(self):
		for i in range(500):
			self.run_stick_cycle()
		for i in range(500):
			self.run_slip_cycle()

	def change_mode(self,mode):
		self.mode = mode

	def set_wall_loc_left(self,loc):
		self.wall_loc_left = loc

	def set_wall_loc_right(self,loc):
		self.wall_loc_right = loc

	def run(self):
		while (self.mode is not None):
			try:
				self.run_cycle(self.mode)
			except KeyboardInterrupt:
				self.clear_motor()
				break

if __name__ == '__main__':
	joystick = user_functions()
	joystick.run()
