#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
 
import os
import requests
from gps import *
from time import *
import time
import threading
import RPi.GPIO as GPIO ## Import GPIO library

import ConfigParser
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

if os.path.exists("/home/pi/pihos/usbconfig.ini") == False:
    print("config.ini error")
    os.system('sudo mount /dev/sda1 /home/pi/pihos/usb')
    exit()
    
Config = ConfigParser.ConfigParser()
Config.read('/home/pi/pihos/usbconfig.ini')

id =  ConfigSectionMap('Profile')['id']
timevdo = ConfigSectionMap('Profile')['timevdo']
timepic = ConfigSectionMap('Profile')['timepic']

 
gpsd = None #seting the global variable

 
os.system('clear') #clear the terminal (optional)
os.system('sudo systemctl stop gpsd.socket')
os.system('sudo systemctl disable gpsd.socket')
os.system('sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock')
os.system('sudo systemctl enable gpsd.socket')
os.system('sudo systemctl start gpsd.socket')

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    
    gpsp.start() # start it up
    countSend = 0
    countError = 0
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
      
      os.system('clear')
      print
      print 'GPS sending Seccess ' , countSend ,' Error ', countError  
      print '----------------------------------------'
      print 'latitude    ' , gpsd.fix.latitude
      print 'longitude   ' , gpsd.fix.longitude
      print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      print 'http://safetyam.tely360.com/api/tracking.php?ambulance_id={0}&tracking_latitude={1:.6f}&tracking_longitude={2:.6f}&tracking_speed={3:.2f}'.format(id,gpsd.fix.latitude,gpsd.fix.longitude,gpsd.fix.speed)
      
      if str(gpsd.fix.latitude) != 'nan' :
        GPIO.output(22,True)
		#userdata = {"busID": "1", "latitude": "Doe", "password": "jdoe123"}
		#resp = requests.post('http://srinuanchan.com/api/bustracking/tracking.php?', params=userdata)
      try:
        #resp = requests.get('http://safetyam.tely360.com/api/tracking.php?ambulance_id={0}&tracking_latitude={1:.6f}&tracking_longitude={2:.6f}&tracking_speed={3:.2f}'.format(3,gpsd.fix.latitude,gpsd.fix.longitude,gpsd.fix.speed), timeout=1.001)
        resp = requests.get('http://safetyam.tely360.com/api/tracking.php?ambulance_id={0}&tracking_latitude={1:.6f}&tracking_longitude={2:.6f}&tracking_speed={3:.2f}'.format(id,gpsd.fix.latitude,gpsd.fix.longitude,gpsd.fix.speed), timeout=1.001)
        #resp = requests.get('http://srinuanchan.com/api/bustracking/tracking.php?busID={0}&latitude={1:.6f}&longitude={2:.6f}&speed={3:.2f}'.format(2,gpsd.fix.latitude,gpsd.fix.longitude,gpsd.fix.speed), timeout=1.001)

        #print 'status_code ' , resp.status_code
        #print 'headers     ' , resp.headers
        print 'content     ' , resp.content
        countSend = countSend + 1
        countError = 0
        GPIO.output(27,True)
      except:
        print 'ConnectionError'
        time.sleep(1)
        countError = countError + 1
        if countError > 20:
          GPIO.output(27,False)
          break
        continue
		
      GPIO.output(22,False)
      time.sleep(0.95) #set to whatever

	  
      
	  
	  #print 'altitude (m)' , gpsd.fix.altitude
      #print 'eps         ' , gpsd.fix.eps
      #print 'epx         ' , gpsd.fix.epx
      #print 'epv         ' , gpsd.fix.epv
      #print 'ept         ' , gpsd.fix.ept
      #print 'speed (m/s) ' , gpsd.fix.speed
      #print 'climb       ' , gpsd.fix.climb
      #print 'track       ' , gpsd.fix.track
      #print 'mode        ' , gpsd.fix.mode
      #print
      #print 'sats        ' , gpsd.satellites
      
	  
	  #r = urllib.request.urlopen('https://api.github.com', auth=('user', 'pass'))
	  #r = requests.get('http://srinuanchan.com/api/bustracking/tracking.php?busID={0}&latitude={1:.6}&longitude={2:.6}&speed={3}'.format(3,gpsd.fix.latitude,gpsd.fix.longitude,gpsd.fix.speed))
	  #r = requests.get('http://srinuanchan.com/api/bustracking/tracking.php?', busID=('1'),latitude=(gpsd.fix.latitude),longitude=(gpsd.fix.longitude),speed=(gpsd.fix.speed))
	  #var r = requests.get('http://www.google.com')
	  
      
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    GPIO.cleanup()
  print "Done.\nExiting."