# RFcontrol
Control of remote mains sockets via 433MHz
Install PiGPIO as follows:
It’s already installed in full fat Raspbian.
If running Raspbian Lite run 
sudo apt install pigpio python-pigpio python3-pigpio
Followed by:
sudo apt install git
git clone https://github.com/joan2937/pigpio
Check what python versions are available (and the default):
ls /usr/bin/python*
python --version
Edit ~/.bashrc to add the python PATH locations and to change the default python version to 3.5 (or whichever the latest version is as displayed above)t:
export PATH=${PATH}:/home/pi:/home/pi/Software:/home/pi/Software/Apps
alias python=’/usr/bin/python3.5’
To activate:
source ~/.bashrc
Check paths:
Echo $PATH
Which will respond with something like:
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games:/home/pi::/home/pi:/home/pi/Software:/home/pi/Software/Apps
As long as ‘xyz.py’ is in one of the above directories, you should now just be able to enter ‘xyz.py’
To run PiGPIO in Python 3, you’ll need to run:
sudo apt install python3-RPi.GPIO
Run pigpiod on boot:
Add this line to the system crontab (sudo crontab –e): 
@reboot /usr/local/bin/pigpiod
Get the Python code for transmitting and decoding 433MHz RF remote codes

wget http://abyz.me.uk/rpi/pigpio/code/_433_py.zip
unzip _433_py.zip
Move the unzipped _433.py to a suitable directory.
Typing (assuming you’ve made the PATH change above)
_433.py 
places the Pi into 433 rx mode, waiting for demodulated FR remote control code on GPIO pin 38.
With the 433MHz receiver connected as below, when a 433MHz remote control is used nearby, something like the following data will be produced:
code=5330005 bits=24 (gap=12780 t0=422 t1=1236)
This data is used by _433.py when used in transmit mode to regenerate the transmission from the remote control.
To pipe this data to a file for later use, run:
_433.py > ~/remotedata.txt 

Dawn-dusk calculator for lights
sudo apt install python3-pip
sudo pip3 install pyephem
sudo apt install python3-crontab
add dawn-dusk.py to cron via 
crontab -e
* 12 * * * python3 /home/pi/Software/Apps/dawn-dusk.py # adds cronjob to run command at dusk
# job added by dawn-dusk.py (variable time of execution determined by sunset time)
# turn off fairy lights
* 21 * * * python /home/pi/Software/Apps/tx.py "fairy lights off" # fairy_lights_off
41 18 * * * python /home/pi/Software/Apps/tx.py "fairy lights on" # fairy_lights_on
