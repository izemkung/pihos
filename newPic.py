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



os.system('sudo rm /home/pi/usb/pic/ch0/*.jpg')  
os.system('sudo rm /home/pi/usb/pic/ch1/*.jpg')
time.sleep(5)
Config = ConfigParser.ConfigParser()
Config.read('/home/pi/usb/config.ini')

id =  ConfigSectionMap('Profile')['id']
timevdo = ConfigSectionMap('Profile')['timevdo']
timepic = ConfigSectionMap('Profile')['timepic']
gps_url = ConfigSectionMap('Profile')['gps_api']
pic_url = ConfigSectionMap('Profile')['pic_api']

OldPic0 = ''
OldPic1 = ''
countError = 0
countPic = 0
countNoNewpic = 0
connectionError = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) ## Use board pin numbering
GPIO.setup(17, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
GPIO.setup(27, GPIO.OUT)#3G
  
while True:
    
    timeout = time.time() + 5

    newpic1 = max(glob.iglob('/home/pi/usb/pic/ch1/*.[Jj][Pp][Gg]'), key=os.path.getctime)
    
    newpic0 = max(glob.iglob('/home/pi/usb/pic/ch0/*.[Jj][Pp][Gg]'), key=os.path.getctime)
    
    if newpic1 != OldPic1 and newpic0 != OldPic0:
        GPIO.output(17,True)
        countNoNewpic = 0
        OldPic0 = newpic0    
        OldPic1 = newpic1
        #try:
            #if OldPic1 != '':
                #os.remove(OldPic1)
                #print 'Delete '+ OldPic1
            #if OldPic0 != '':
                #os.remove(OldPic0)
                #print 'Delete '+ OldPic0
            #OldPic0 = newpic0    
            #OldPic1 = newpic1
        #except:
            #print 'Error no such file'
        #print 'Send ' +newpic0
        #print 'Send ' +newpic1
        
        
        with open(newpic1, "rb") as image_file1:
            encoded_string1 = base64.b64encode(image_file1.read())
        with open(newpic0, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            
        data = {'ambulance_id':id,'images_name_1':encoded_string1,'images_name_2':encoded_string}
        try:
            r = requests.post(pic_url, data=data)
            #print r
            #print 'Send '
            GPIO.output(27,True)
            GPIO.output(17,False)
            countPic += 1
            
            connectionError = 0
        except:
            GPIO.output(27,False)
            connectionError += 1
            if connectionError > 10:
                print "Connection Error"
                break    
            
    else:
        countNoNewpic += 1
         
    if countNoNewpic > 20 :
        GPIO.output(17,False)
        print "No new pic upadte"
        break
      
            
    time.sleep(0.2)
    if time.time() > timeout:
        print "Timeout"
        break

GPIO.output(17,False)   
GPIO.cleanup()