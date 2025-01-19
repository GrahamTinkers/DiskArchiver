#!/usr/bin/env python
#
# Author: Graham Hooley
#Filename: disk_copy.py
#Description: This code works with the mechanical disk duplicator that was repurposed for the project;
# the code controls the mechanical mechanism, the Greaseweazle, and Pi Camera 2
#########################################################################################################

import argparse
import time
import serial
import subprocess
import random
import os
import sys
from picamera2 import Picamera2, Preview
import RPi.GPIO as GPIO
import pwd
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# Set up the GPIO pins
led_pin = 5
GPIO.setup(led_pin, GPIO.OUT)
# Initialize the camera
os.environ["LIBCAMERA_LOG_LEVELS"] = "3"
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (800, 600)})
picam2.configure(camera_config)
picam2.start()
#__dest_path = '/media/graham/ESD-USB/'
# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-c", "--Command", help = "Send Command")

# Read arguments from command line
args = parser.parse_args()

class sercom:
	accept          = 'A' # Accept disk, disk are droped into the front bim
	insert          = 'I' # Insert disk
	reject          = 'R' # Reject disk, disks are dropped into the reject bin on the left of the system
	calibrate       = 'C' # Calibrate the device
	complete        = 'X' # X is returned if if the commands A, I, R, C are completed
	error           = 'E' # Returned if an error occours
	undefined       = '?' # Returned if an unknown status is returned
	status          = 'S' # Return the status of the device
	version         = 'O' # Returns the firmware version
	diskcount       = 'V' # Returns the number of disks processed

# Status codes
# 0000 Normal
# 0001 Disk jammed
# 0010 Imput hopper empty
# 0100 Command out of sequence
# 1000 Calibration error
# 1001 Disk stuck in drive, or jamed in mech
# 1100 Disk sent to accept bin when it should have gone to the reject bin
# 1101 Reject bin full

# 07 Home - Normal, recived after C, R, A
# 0B Insert - Normal, received after I
# 17 Jam - Received after I
# 27 Hopper empty received after  I
# 47, 4B Command Out of Sequence - Received after I
# 87 Calibration Error - Received after unsecessful C command
# 97 Disk In Drive - Returned after unsucessful A command
# C7 Reject error - Disk went to accept insted of Reject
# DB Output Bin Full
fn = "default.jpg"
disk_format = "amiga.amigados"

# Get the current username; used by the get_removable_media() function
def get_username():
        return pwd.getpwuid(os.getuid())[0]

def get_removable_media():
        # Assume the /media folder exists and add the current username to the path and get any mounted device;
        # there should be only one USB Storage media inserted; if no device exists, then default to ~/
        destination_path = '/media/default/' # Fake value
        path = '/media/' + get_username() + '/'
        dir = os.listdir(path)

        for dirs in dir:
                destination_path = (path + str(dirs))

        if not os.path.isdir(destination_path):
                destination_path = '~/'
        return destination_path + '/'
destination_path = get_removable_media()

# Setup serial port
ser = serial.Serial(
	port='/dev/ttyUSB0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
	baudrate = 9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

def funtion_photo_disk(file_name):
	GPIO.output(led_pin, GPIO.HIGH)
	time.sleep(.2)
	picam2.capture_file(file_name + '.jpg')
	time.sleep(.1)
	GPIO.output(led_pin, GPIO.LOW)

def function_check_status():
	ser.write(sercom.status.encode())
	time.sleep(.5)
	#ser.flushInput()
	x = ser.readline().decode('utf-8').strip()
	return x

def function_load_disk():
	ser.write(sercom.insert.encode())

def fuction_accept_disk():
	global fn
	ser.write(sercom.accept.encode())
	time.sleep(1)
	funtion_photo_disk(fn)

def function_reject_disk():
	ser.write(sercom.reject.encode())


def function_read_disk():
	global fn
	fn = function_filename()
	x = subprocess.run(['gw', 'read', '--format=' + disk_format, fn, '--raw', '--drive=B'])
	return x.returncode

def function_filename():
	global fn
	fe = True
	while fe == True:
		n = random.randint(0,10000)
		fn = destination_path + disk_format + '_DiskImage{0:04d}.scp'.format(n)
		#fn = __dest_path + 'DiskImage{0:04d}.scp'.format(n)
		fe = os.path.isfile(fn)
		if fe == False:
			return fn

def clean_up():
	ser.write(sercom.reject.encode())
	GPIO.cleanup()
	picam2.close()
	ser.write(sercom.calibrate.encode())
	ser.close()
	sys.exit(0)
	print('Aborting')

def main():
	#command = 'L'
	time.sleep(.2)
	ret_code = function_check_status()
	#print ('Status code is ' + str([ret_code]))
	time.sleep(.2)
	ret_code = function_check_status()
	print ('Status code after .2 second delay ' + str([ret_code]))
	if ((ret_code == '07' or ret_code == '0B')):
	#if ((ret_code == '\x007' or ret_code == '07') and (command == 'L')):
		print ('Load Disk....')
		function_load_disk()
		time.sleep(.2)
		ret_code = function_check_status()
		time.sleep(.2)
		ret_code = function_check_status()
		print ('Disk load status' + str([ret_code]))
		if (ret_code == '0B'):
			print ('Read Disk....')
			disk_read = function_read_disk()
			print ('Read complete, status code')
			print (disk_read)
			if (disk_read == 0):
				print ('Disk Accepted....')
				fuction_accept_disk()
			else:
				print ('Disk Rejected....')
				function_reject_disk()
	else:
		print ('Error, return code is ' + str([ret_code]))
		if (ret_code == '27'):
                       print ('Hopper empty, add disks')
		if (ret_code == '17'):
			print ('Disk jam, clear jammed disk')
		if (ret_code == '47' or ret_code == '4B'):
			print ('Command out of sequence after disk insertion')
		if (ret_code == '87'):
			print ('Calibration error')
		if (ret_code == 'C7'):
			print ('Reject error, disk was accepted insted of being rejected')
		if (ret_code == '97'):
			print ('Disk in drive, eject the disk')
		if (ret_code == 'DB'):
			print ('Output fopper full')
		clean_up()
	global fn
	filename = fn
	#print(filename)

try:
	count = 0
	while (count < 20):
		main()
		count += 1
	else:
		GPIO.cleanup()
		picam2.close()
		ser.close()
		print('Job complete, exiting')

except KeyboardInterrupt:
	GPIO.cleanup()
	picam2.close()
	ser.write(sercom.reject.encode())
	ser.close()
	print('Aborting')
