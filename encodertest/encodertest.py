
import usb.core
import time

class encodertest:

    def __init__(self):
        self.TOGGLE_LED1 = 0
        self.TOGGLE_LED2 = 1
        self.TOGGLE_LED3 = 2
        self.READ_SW1 = 3
        self.READ_SW2 = 4
        self.READ_SW3 = 5
        self.ENC_READ_REG = 6
        self.dev = usb.core.find(idVendor = 0x6666, idProduct = 0x0003)
        self.startangle = 0
        self.prev_angle = 0
        self.total_angle = 0
        if self.dev is None:
            raise ValueError('no USB device found matching idVendor = 0x6666 and idProduct = 0x0003')
        self.dev.set_configuration()

# AS5048A Register Map
        self.ENC_NOP = 0x0000
        self.ENC_CLEAR_ERROR_FLAG = 0x0001
        self.ENC_PROGRAMMING_CTRL = 0x0003
        self.ENC_OTP_ZERO_POS_HI = 0x0016
        self.ENC_OTP_ZERO_POS_LO = 0x0017
        self.ENC_DIAG_AND_AUTO_GAIN_CTRL = 0x3FFD
        self.ENC_MAGNITUDE = 0x3FFE
        self.ENC_ANGLE_AFTER_ZERO_POS_ADDER = 0x3FFF

    def close(self):
        self.dev = None

    def toggle_led1(self):
        try:
            self.dev.ctrl_transfer(0x40, self.TOGGLE_LED1)
        except usb.core.USBError:
            print "Could not send TOGGLE_LED1 vendor request."

    def toggle_led2(self):
        try:
            self.dev.ctrl_transfer(0x40, self.TOGGLE_LED2)
        except usb.core.USBError:
            print "Could not send TOGGLE_LED2 vendor request."

    def toggle_led3(self):
        try:
            self.dev.ctrl_transfer(0x40, self.TOGGLE_LED3)
        except usb.core.USBError:
            print "Could not send TOGGLE_LED3 vendor request."

    def read_sw1(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.READ_SW1, 0, 0, 1)
        except usb.core.USBError:
            print "Could not send READ_SW1 vendor request."
        else:
            return int(ret[0])

    def read_sw2(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.READ_SW2, 0, 0, 1)
        except usb.core.USBError:
            print "Could not send READ_SW2 vendor request."
        else:
            return int(ret[0])

    def read_sw3(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.READ_SW3, 0, 0, 1)
        except usb.core.USBError:
            print "Could not send READ_SW3 vendor request."
        else:
            return int(ret[0])

    def enc_readReg(self, address):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.ENC_READ_REG, address, 0, 2)
        except usb.core.USBError:
            print "Could not send ENC_READ_REG vendor request."
        else:
            return ret

    def get_angle(self):
        try:
            ret = self.dev.ctrl_transfer(0xC0, self.ENC_READ_REG, 0x3FFF, 0, 2)
        except usb.core.USBError:
            print "Could not send ENC_READ_REG vendor request."
        else:
            return (int(ret[0]) + 256 * int(ret[1])) & 0x3FFF

    def get_angle_trans_int(self):
    	angle_raw = int(self.get_angle())
    	angle_out = int(angle_raw)
    	angle_out =-0.0221*angle_out + 361
    	return angle_out

    def record_angle(self):
    	f = open("test_data_attachment.csv",'w')
    	starttime = time.time()
    	for i in range (5000):
    		f.write(str('{:d}'.format(self.get_angle())) + ',' + str(time.time()-starttime) + ';')
    		f.write('\n')
    		time.sleep(0.0005)

    def get_delta_angle(self):
    	curr_angle = self.get_angle_trans_int()
    	delta_angle = curr_angle - self.prev_angle
        if (delta_angle > 100):
            delta_angle = delta_angle - 360
        elif (delta_angle < -100):
            delta_angle = delta_angle + 360
    	self.total_angle = self.total_angle + delta_angle
    	self.prev_angle = curr_angle
    	return delta_angle

    def track_angle(self):
        self.total_angle = float(self.total_angle) + self.get_delta_angle()
        return self.total_angle
    	



if __name__ == '__main__':
	Encoder = encodertest()
	#Encoder.record_angle()
	while True:
		print Encoder.track_angle()
		time.sleep(0.0005)
