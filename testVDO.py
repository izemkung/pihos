from time import gmtime, strftime
import time
import datetime
import imutils
import numpy as np
import cv2
import argparse
import os

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

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="/home/pi/usb/",
	help="path to output")
ap.add_argument("-i", "--idcamera", type=int, default=0,
	help="camera should be used")
ap.add_argument("-t", "--timevdo", type=int, default=timevdo,
	help="time of output video(min)")
ap.add_argument("-c", "--timepic", type=float, default=timepic,# 0.95
	help="save pic evev sec(sec)")
args = vars(ap.parse_args())

if os.path.exists(args["output"]+"vdo/ch0") == False:
    print("Mkdir!!!")
    #os.system('sudo mount /dev/sda1 /mnt/usbdrive')
    os.system('sudo mkdir /home/pi/usb/vdo')
    os.system('sudo mkdir /home/pi/usb/vdo/ch0')
    os.system('sudo mkdir /home/pi/usb/vdo/ch1')
    os.system('sudo mkdir /home/pi/usb/pic')
    os.system('sudo mkdir /home/pi/usb/pic/ch0')
    os.system('sudo mkdir /home/pi/usb/pic/ch1')
    exit()
       
print("Camera "+str(args["idcamera"])) 

cap = cv2.VideoCapture(args["idcamera"])

#set the width and height, and UNSUCCESSFULLY set the exposure time
#Config 
timeSavePic = args["timepic"]
timeVDO = args["timevdo"]

cap.set(3,1360/2)
cap.set(4,768/2)
cap.set(5,20)
#cap.set(3,1024)
#cap.set(4,768)

#time.sleep(2)

#cap.set(15, -8.0)
#cap.set(15, 0.1)

# Define the codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC('D','I','V','X')

ret, frame = cap.read()
(h, w) = frame.shape[:2]
print("Vdo:"+str(w)+"x"+str(h) + " Pic:"+str(w/4)+"x"+str(h/4) )

vdoname =  gmtime()
out = cv2.VideoWriter(args["output"]+ 'vdo/ch' +str(args["idcamera"]) +'/vdo_{}.avi'.format(strftime("%d%m%Y%H%M%S", vdoname)),fourcc, 20.0, (w,h))
print(args["output"]+ 'vdo/ch' +str(args["idcamera"]) +'/vdo_{}.avi'.format(strftime("%d%m%Y%H%M%S", vdoname))) 

#Picture 
current_time = 0
countPic = 0
endtime = 0
framePic = None 
startTime = time.time()


while(cap.isOpened()):
    current_time = time.time()
 
    ret, frame = cap.read()
    if ret==True:
        if current_time - endtime > timeSavePic:
            framePic = imutils.resize(frame, w/4)    
            cv2.imwrite(args["output"]+  'pic/ch' +str(args["idcamera"])  +'/img_{}.jpg'.format(strftime("%d%m%Y%H%M%S", gmtime())), framePic)
            endtime = current_time
            countPic+=1
            
        out.write(frame)
        #cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if current_time - startTime > 60*timeVDO:
            break 
    else:
        break

# Release everything if job is finished
print("Time > "+str(timeVDO) + " m NumPic > "+str(countPic)) 
print("Process time > "+str(current_time - startTime)+" sec")
out.release()
cap.release()
print("Ok!!!") 