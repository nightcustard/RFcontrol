#!/usr/bin/python3
# coding=utf-8

# tx.py
# Uses pigpio library and python programme _433.py to transmit remote control signals to remote mains sockets.
# Can be used as tx.py, in which case the menu is presented, or tx.py "command" which will execute the text command directly.

import sys
import time
import pigpio
import _433
import datetime
import os
import subprocess

TX=21  #GPIO pin 40
pi = pigpio.pi()

# Tuple is indexed 0 to 234 ( in this case)
# Remote control codes tuple. Each group of five corresponds to a remote command (eg) 0 to 4 is I-1on, 5 to 9 is I-1off etc. Index 0 to 159 covers the Wilco RSL366T remote, 160 to 189 the AEI_RA103 remote and 190 to 234 covers the Status_RCT08 remote.
# The Wilco remote has 32 different commands, numbered I-1 to I_4 (on/off), II, III & IV; The AEI has six (1 to 3 on/off); the Status has nine (1 to 4 on/off and all off)

remote = (1381717, 24, 12770, 420, 1229, 1381716, 24, 12775, 412, 1237, 1394005, 24, 12800, 411, 1237, 1394004, 24, 12760, 420, 1228, 1397077, 24, 12750, 413, 1236, 1397076, 24, 12800, 413, 1238, 1397845, 24, 12760, 422, 1226, 1397844, 24, 12790, 416, 1232, 4527445, 24, 12770, 413, 1235, 4527444, 24, 12750, 411, 1239, 4539733, 24, 12770, 408, 1240, 4539732, 24, 12760, 405, 1244, 4542805, 24, 12770, 405, 1242, 4542804, 24, 12795, 413, 1235, 4543573, 24, 12760, 418, 1230, 4543572, 24, 12735, 422, 1226, 5313877, 24, 12785, 418, 1230, 5313876, 24, 12730, 415, 1233, 5326165, 24, 12780, 420, 1229, 5326164, 24, 12760, 417, 1231, 5329237, 24, 12770, 413, 1236, 5329236, 24, 12750, 416, 1233, 5330005, 24, 12785, 415, 1233, 5330004, 24, 12760, 410, 1240, 5510485, 24, 12805, 408, 1242, 5510484, 24, 12795, 417, 1231, 5522773, 24, 12805, 411, 1237, 5522772, 24, 12795, 420, 1228, 5525845, 24, 12770, 409, 1239, 5525844, 24, 12770, 417, 1232, 5526613, 24, 12790, 415, 1233, 5526612, 24, 12810, 413, 1235, 5522517, 24, 10970, 353, 1064, 1328212, 24, 10966, 365, 1052, 5526613, 24, 10960, 358, 1062, 1332308, 24, 10970, 360, 1058, 5521749, 24, 10985, 353, 1065, 1327444, 24, 10980, 358, 1060, 616895, 24, 9600, 303, 911, 616887, 24, 9615, 300, 913, 616891, 24, 9625, 298, 916, 616883, 24, 9610, 303, 911, 616893, 24, 9640, 300, 914, 616885, 24, 9575, 306, 908, 616894, 24, 9640, 299, 916, 616886, 24, 9575, 301, 913, 616888, 24, 9585, 299, 915)

# 'command' tuple.  Contains the designated remote control text followed by the index of the associated remote control parameters contained in the 'remote' tuple
# 80 corresponds to Wilco remote control III-1 on; 85 to III-1 off; 90 to III-2 on; 95 to III-2 off; 100 to III-3 on; 105 to III-3 off; 170 to AEI-2 on; 175 to AEI-2 off; 120 to WIV-1 on; 125 to WIV-1 off; 40 to WII-1 on; 45 to WII-1 off; 50 to WII-2 on; 55 to WII-2 off' (see end of file for current allocations)
# Remote control parameters were captured using a 433MHz rx and _433.py 
# Commands must be in same order as the menu below and can be moved (as a pair - text and index number) to suit menu order. Can substitute any text for placeholder text (eg) "WII-2on" can be "lights on"

command = ("fairy lights on", 80, "fairy lights off", 85, "porch fairy lights on", 90, "porch fairy lights off", 95, "porch lights on", 100, "porch lights off", 105, "Amp on", 170, "Amp off", 175, "front room lamp on", 110, "front room lamp off", 115, "stairs fairy lights on", 70, "stairs fairy lights off", 75, "Ikea kitchen lights on", 40, "Ikea kitchen lights off", 45, "Xmas lights on", 50, "Xmas lights off", 55, "Xmas tree lights on", 60, "Xmas tree lights off", 65, "WI-1on", 0, "WI-1off", 5, "WI-2on", 10, "WI-2off", 15, "WI-3on", 20, "WI-3off", 25, "WI-4on", 30, "WI-4off", 35, "WIV-1on", 120, "WIV-1off", 125, "WIV-2on", 130, "WIV-2off", 135, "WIV-3on", 140, "WIV-3off", 145, "WIV-4on", 150, "WIV-4off", 155, "AEI-1on", 160, "AEI-1off", 165, "AEI-3on", 180, "AEI-3off", 185, "Status-1on", 190, "Status-1off", 195, "Status-2on", 200, "Status-2off", 205, "Status-3on", 210, "Status-3off", 215, "Status-4on", 220, "Status-4off", 225, "Status-alloff", 230) 

t = 3  # time delay between switching white lights off and then back on again (to allow lights controller to settle)

if not pi.connected:
	exit()

def tx():    # _433.tx sends the appropriate remote control codes to the 433MHz transmitter
	tx=_433.tx(pi, gpio=TX, gap=remote[i+2], t0=remote[i+3], t1=remote[i+4])
	for p in range (5):		# send code five times
		tx.send(remote[i])
	tx.cancel()

def help():
	print("\nUsage: tx.py (to get menu) or tx.py 'command' - note the use of '', where valid commands are:")
	print("\n'fairy lights on',\n'fairy lights off',\n'porch fairy lights on',\n'porch fairy lights off',\n'porch lights on',\n'porch lights off',\n'Amp on',\n'Amp off',\n'front room lamp on',\n'front room lamp off',\n'stairs fairy lights on',\n'stairs fairy lights off',\n'Ikea kitchen lights on',\n'Ikea kitchen lights off',\n'Xmas lights on',\n'Xmas lights off'\n'Xmas tree lights on',\n'Xmas tree lights off',\n") # add to list as appropriate   

# This section looks for one or more command line arguments and executes each in turn, thus permitting multiple commands to be executed at the same time

if len(sys.argv) >= 2: # Check for one or more command line arguments, if none go to menu section below. 
	n = len(sys.argv)-1 # n = number of command line arguments
	for x in range(n): # x runs from 0 to n-1
		G = sys.argv[x+1] #[0] is /home/pi/Software/Apps/tx.py; [1] is (eg) fairy lights on; [2] is second command line argument etc.
		try:                         # allows errors to be handled
			index = command.index(G) # return the index of the text in the command tuple, if it isn't there, then:
		except ValueError:           # a ValueError is returned if the input isn't in the command tuple
			print('\033[1;31;40mInput not recognised, please try again.\n')  #see end for explanation of ANSI escape sequence
			help()
			exit()

		i = command[index+1]  # i is the start index position of the five remote control codes in the 'remote' tuple
		tx()
	exit()	
		
# This is the text prompt menu section if no command line arguments were entered
else:
	
	print("\n\033[1;36;40mWelcome to RF remote Pi\n")
	print("\n\033[1;36;40mPlease enter the number corresponding to what you want to do.\n")
	print("\033[1;36;40mEnter 1 to switch house fairy lights on.")
	print("\033[1;36;40mEnter 2 to switch house fairy lights off.")
	print("\033[1;36;40mEnter 3 to switch porch fairy lights on.")
	print("\033[1;36;40mEnter 4 to switch porch fairy lights off.")
	print("\033[1;36;40mEnter 5 to switch porch white lights on.")
	print("\033[1;36;40mEnter 6 to switch porch white lights off.") 
	print("\033[1;36;40mEnter 7 to switch kitchen audio amp on.")
	print("\033[1;36;40mEnter 8 to switch kitchen audio amp off.")
	print("\033[1;36;40mEnter 9 to switch front room lamp on.")
	print("\033[1;36;40mEnter 10 to switch front room lamp off.")
	print("\033[1;36;40mEnter 11 to switch stairs fairy lights on.")
	print("\033[1;36;40mEnter 12 to switch stairs fairy lights off.")
	print("\033[1;36;40mEnter 13 to switch Ikea kitchen lights on.")
	print("\033[1;36;40mEnter 14 to switch Ikea kitchen lights off.")
	print("\033[1;36;40mEnter 15 to switch Xmas lights on.")
	print("\033[1;36;40mEnter 16 to switch Xmas lights off.")
	print("\033[1;36;40mEnter 17 to switch Xmas tree lights on.")
	print("\033[1;36;40mEnter 18 to switch Xmas tree lights off.")
	print("\033[1;36;40mEnter any other key or number to quit.\n")

	b = 1
	n = 18  # when adding more commands, n is the number of commands
	while (b > 0) and (b < n+1):  
		try:
			b = int(input("\033[0;37;40mWhat would you like to do? "))
		except ValueError:
			print('\033[1;31;40mTerminating')
			break
		if (b <= 0) or (b > n):  # when adding more commands, n in (b > n) is the number of commands
			break
		else:
			inp = b-2
			B = b+inp
			G = command[B]  # Tells the print command below what the command is (eg) "fairy lights off"
			index = command.index(G) # Gives the index number of the command in the command tuple
			i = command[index+1]  # i is the start index position of the five remote control codes in the 'remote' tuple
			print('\033[0;32;40mTurning', G, '\n')   
			tx()

exit()

#Troubleshooting:
#print('Index of G:', index)
#print('remote[i]', remote[i])
#print('remote[i+1]', remote[i+1])
#print('remote[i+2]', remote[i+2])
#print('remote[i+3]', remote[i+3])
#print('remote[i+4]', remote[i+4])

#ANSI escape codes

#format is: \033[  Escape code; 1 = Style; 31 = Text colour (red); 40m = Background colour (black)
#TEXT COLOR	TEXT STYLE		BACKGROUND COLOR
#Black	30	No effect	0	Black	40
#Red	31	Bold		1	Red	41
#Green	32	Underline	2	Green	42
#Yellow	33	Negative1	3	Yellow	43
#Blue	34	Negative2	5	Blue	44
#Purple	35				Purple	45
#Cyan	36				Cyan	46
#White	37				White	47

#	Remote control allocation
#fairy lights (+ mirror lights)on/off:			WIII-1
#porch fairy lights on/off:				WIII-2
#porch lights on/off:					WIII-3
#Kitchen Amp on/off:					AEI-2
#front room lamp on/off:				WIII-4
#Ikea kitchen lights on/off:				WII-1
#Xmas & front door lights on/off:			WII-2
#Xmas tree lights on/off:				WII-3
#Stairs fairy lights on/off:				WII-4
