#!/usr/bin/env python
#
# Author: Graham Hooley aka Graham Tinkers
# Filename: disk_com.py
# Description: This code works with the mechanical disk duplicator that was repurposed for the project;
# the code controls the mechanical mechanism by you can sending commands over the serial port.
#
# Usage: disk_com.py -c I # This would inster a disk
#
#########################################################################################################
import argparse
import time
import serial
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


# Setup serial port
ser = serial.Serial(
        port='/dev/ttyUSB0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

def function_read_disk():
	ser.write(args.Command.encode())
	print (args.Command.encode())
	time.sleep(.1)
	x=ser.readline().decode('utf-8').rstrip()
	print (x)
    ser.close()

function_read_disk()
