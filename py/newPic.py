import os
import glob
import cv2
import cv
import datetime
import base64
import requests
import urllib2
import httplib
import time
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

if os.path.exists("/home/pi/usb/config.ini") == False:
    print("config.ini error")
    os.system('sudo mount /dev/sda1 /home/pi/usb/')
    exit()
    
Config = ConfigParser.ConfigParser()
Config.read('/home/pi/usb/config.ini')

id =  ConfigSectionMap('Profile')['id']
timevdo = ConfigSectionMap('Profile')['timevdo']
timepic = ConfigSectionMap('Profile')['timepic']

OldPic0 = ''
OldPic1 = ''
#url = 'http://srinuanchan.com/api/bustracking/upload.php'
url = 'http://safetyam.tely360.com/api/upload.php'
countError = 0
countNoNewpic = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) ## Use board pin numbering
GPIO.setup(17, GPIO.OUT) ## Setup GPIO Pin 7 to OUT

  
while True:
    newpic0 = max(glob.iglob('/home/pi/usb/pic/ch0/*.[Jj][Pp][Gg]'), key=os.path.getctime)

    newpic1 = max(glob.iglob('/home/pi/usb/pic/ch1/*.[Jj][Pp][Gg]'), key=os.path.getctime)

    try:
        if newpic0 != OldPic0:
            GPIO.output(17,True)
            print '17 On'
            countNoNewpic = 0
            OldPic0 = newpic0
            print newpic0
            with open(newpic0, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                data = {'ambulance_id':id,'images_name_1':encoded_string}
                r = requests.post(url, data=data)
                print r
        else:
            countNoNewpic += 1
                
        if newpic1 != OldPic1:
            GPIO.output(17,True)
            countNoNewpic = 0
            OldPic1 = newpic1
            print newpic1
            with open(newpic1, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                data = {'ambulance_id':id,'images_name_1':encoded_string}
                r = requests.post(url, data=data)
                print r
        else:
            countNoNewpic += 1
            
        if countNoNewpic > 10 :
            GPIO.output(17,False)
            print '17 Off'
        countError = 0
        
    except:
        print 'ConnectionError'
        time.sleep(1)
        countError = countError + 1
        if countError > 20:
            print 'ConnectionError > 20'
            break

        continue
            
    time.sleep(0.5)
    
GPIO.cleanup()