# coding=utf-8
#!/usr/bin/python3
# dawn-duskRFR.py (Radio Frequency Remotes)
# code from https://www.raspberrypi.org/forums/viewtopic.php?t=114745
# Determines time of sunrise & sunset for given lat/long and adds line to user crontab to switch on lights
# at dusk

import ephem
import datetime

home = ephem.Observer() # See: https://rhodesmill.org/pyephem/quick.html
home.lat = '53.451188' # Culcheth latitude from Google maps
home.lon = '-2.527018' # Culcheth longitude from Google maps
home.elevation = 36  # Langcliffe Close altitude from https://www.daftlogic.com/sandbox-google-maps-find-altitude.htm#
print ('Current date and UTC time is ',home.date)

sun = ephem.Sun()
r1 = home.next_rising(sun)
r1 = ephem.localtime(r1) # converts UTC time returned by ephem to local time in datetime.datetime format
#r1 = r1 - datetime.timedelta(minutes=30) # subtracts 30 minutes so camera settings match light level (see: https://stackoverflow.com/questions/100210/what-is-the-standard-way-to-add-n-seconds-to-datetime-time-in-python)
r1 = datetime.datetime.strptime(str(r1), "%Y-%m-%d %H:%M:%S.%f")  # splits str(r1) into component parts (see: https://stackoverflow.com/questions/33810980/date-time-split-in-python)
# components are: r1.year; r1.month; r1.day; r1.hour; r1.minute; r1.second

s1 = home.next_setting(sun)
s1 = ephem.localtime(s1) # converts UTC time returned by ephem to local time in datetime.datetime format
s1 = s1 + datetime.timedelta(minutes=30) # adds 30 minutes so camera settings match light level
s1 = datetime.datetime.strptime(str(s1), "%Y-%m-%d %H:%M:%S.%f")  # splits str(s1) into component parts
# components are: s1.year; s1.month; s1.day; s1.hour; s1.minute; s1.second

home.horizon = '-0:34'
r2 = home.next_rising(sun)
s2 = home.next_setting(sun)
#print ("Visual sundawn (local time) %s" % r1)
#print ("Visual sunset (local time) %s" % s1)
#print ("Naval obs sundawn %s" % r2)
#print ("Naval obs sunset %s" % s2)
#print(s1)  #2018/8/23 19:21:15


from crontab import CronTab
cron = CronTab(user='pi')

duskhour = s1.hour
duskmin = s1.minute

dawnhour = r1.hour
dawnmin = r1.minute

cron.remove_all(comment='Amp_off') #deletes all jobs with matching comments to prevent multiple lines being generated
cron.remove_all(comment='fairy_lights_on')
cron.remove_all(comment='fairy_lights_off')
cron.remove_all(comment='front_room_lamp_on')
cron.remove_all(comment='front_room_lamp_off')
cron.remove_all(comment='xmas_white_tree_lights_on')
cron.remove_all(comment='xmas_white_tree_lights_off')
cron.remove_all(comment='xmas_lights_on')
cron.remove_all(comment='xmas_lights_off')
cron.remove_all(comment='xmas_green_tree_lights_on')
cron.remove_all(comment='xmas_green_tree_lights_off')
cron.remove_all(comment='stairs fairy_lights_on')
cron.remove_all(comment='stairs fairy_lights_off')

#All times below mustn't overlap as you can't transmit two codes simultaneously.
if duskmin == 59:  # prevents duskmin +1 (see below) = 60 (which is an invalid value)
	duskmin = 58

# House fairy lights, Front room lamp & Kitchen amp off time
FLoffhr = 23
FLoffmin = 0

# Christmas tree lights on time
treeonhr = 06
treeonmin = 45

#Turns off the house fairy lights, front room lamp, stairs fairy lights & kitchen amp at 23:00
job = cron.new(command='python3 /home/pi/Software/Apps/tx.py "fairy lights off" "front room lamp off" "Amp off" "stairs fairy lights off"', comment='fairy_lights_off')
job.hour.on(FLoffhr)
job.minute.on(FLoffmin)

#Fairy lights ON:  These are set to come on at 06:45 in crontab but as a fall-back, are also turned on at dusk. Front room lamp, Xmas lights also turned on
job = cron.new(command='python3 /home/pi/Software/Apps/tx.py "fairy lights on" "front room lamp on" "Xmas lights on"', comment='fairy_lights_on')
job.hour.on(duskhour)
job.minute.on(duskmin)

#Stairs Fairy lights ON
job = cron.new(command='python3 /home/pi/Software/Apps/tx.py "stairs fairy lights on"', comment='stairs fairy_lights_on')
job.hour.on(6)
job.minute.on(0)

#Outside Xmas lights, inside Xmas tree lights OFF
job = cron.new(command='python3 /home/pi/Software/Apps/tx.py "Xmas lights off" "Xmas green tree lights off" "Xmas white tree lights off"', comment='xmas_lights_off')
job.hour.on(22)
job.minute.on(0)

#Green Xmas tree lights ON (come on at 06:45)
job = cron.new(command='python3 /home/pi/Software/Apps/tx.py "Xmas green tree lights on" "Xmas white tree lights on"', comment='xmas_green_tree_lights_on')
job.hour.on(treeonhr)
job.minute.on(treeonmin)

#Xmas white tree lights 
#These lights switch off automatically every 4 or 5 hours - need to recycle power to turn lights back on.
#Come on at 06:45, recycle power every 4 hours, switch off at 22:00
h = treeonhr
m = treeonmin

while (h<22):
	h=h+4
	job = cron.new(command='python3 /home/pi/Software/Apps/tx.py "Xmas white tree lights on"', comment='xmas_white_tree_lights_on') # cycles power to white lights (off then on)
	job.hour.on(h)
	job.minute.on(m)
	
cron.write()  #writes new user crontab
