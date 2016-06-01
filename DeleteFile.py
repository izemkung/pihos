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
import sys

if os.path.exists("/home/pi/pihos/usb/vdo/ch0") == False:
    os.system('sudo mount /dev/sda1 /home/pi/pihos/usb')
    print 'Mount!!!'
    exit()
    
statvfs = os.statvfs('/home/pi/pihos/usb')
size = (statvfs.f_frsize * statvfs.f_blocks) / 1073741824.00
avail = (statvfs.f_frsize * statvfs.f_bavail) / 1073741824.00 
per = (( size - avail ) / size ) * 100
print '/home/pi/usb  Size = {0:.2f} Avail = {1:.2f} Use% = {2:.2f}'.format(size,avail,per)

#================================Delet PIC==================================
#print len([name for name in os.listdir('/home/pi/usb/pic/ch0') if os.path.isfile(os.path.join('/home/pi/usb/pic/ch0', name))])
#print min(glob.iglob('/home/pi/usb/pic/ch0/*.[Jj][Pp][Gg]'), key=os.path.getctime)
count = 0 
if len([name for name in os.listdir('/home/pi/pihos/usb/pic/ch0') if os.path.isfile(os.path.join('/home/pi/pihos/usb/pic/ch0', name))]) > 7200 :
    print 'NUM Pic ch0 > 7000 '
    while len([name for name in os.listdir('/home/pi/pihos/usb/pic/ch0') if os.path.isfile(os.path.join('/home/pi/pihos/usb/pic/ch0', name))]) > 3600: 
       pic0 = min(glob.iglob('/home/pi/pihos/usb/pic/ch0/*.[Jj][Pp][Gg]'), key=os.path.getctime)
       count += 1
       os.remove(pic0)
    print 'Delete {0} file in /home/pi/pihos/usb/pic/ch0/ '.format(count)
       
count = 0    
if len([name for name in os.listdir('/home/pi/pihos/usb/pic/ch1') if os.path.isfile(os.path.join('/home/pi/pihos/usb/pic/ch1', name))]) > 7200:
    print 'NUM Pic ch1 > 7000 '
    while len([name for name in os.listdir('/home/pi/pihos/usb/pic/ch1') if os.path.isfile(os.path.join('/home/pi/pihos/usb/pic/ch1', name))]) > 3600:
       pic1 = min(glob.iglob('/home/pi/pihos/usb/pic/ch1/*.[Jj][Pp][Gg]'), key=os.path.getctime) 
       count += 1
       os.remove(pic1)
    print 'Delete {0} file in /home/pi/pihos/usb/pic/ch1/ '.format(count)
    
if per < 80 :
    time.sleep(300)
    print 'Memmory is < 80% Ok!!'
    exit()
    
while per > 70 :

    OldVideo0 = min(glob.iglob('/home/pi/pihos/usb/vdo/ch0/*.[Aa][Vv][Ii]'), key=os.path.getctime)
    OldVideo1 = min(glob.iglob('/home/pi/pihos/usb/vdo/ch1/*.[Aa][vv][Ii]'), key=os.path.getctime)

    count = 0
    for file in os.listdir("/home/pi/pihos/usb/pic/ch0/"):
        if file.endswith(".jpg"):
            if os.path.getctime("/home/pi/pihos/usb/pic/ch0/" + file) < os.path.getctime(OldVideo0) :
                os.remove("/home/pi/pihos/usb/pic/ch0/" + file)
                count = count +1

    os.remove(OldVideo0)
    print 'Delete '+ OldVideo0 
    print 'Delete {0} file in /home/pi/pihos/usb/pic/ch0/ '.format(count)

    count = 0;
    for file in os.listdir("/home/pi/pihos/usb/pic/ch1/"):
        if file.endswith(".jpg"):
            if os.path.getctime("/home/pi/pihos/usb/pic/ch1/" + file) < os.path.getctime(OldVideo1) :
                os.remove("/home/pi/pihos/usb/pic/ch1/" + file)
                count = count +1
                
    os.remove(OldVideo1)
    print 'Delete '+ OldVideo1       
    print 'Delete {0} file in /home/pi/pihos/usb/pic/ch1/ '.format(count)

    statvfs = os.statvfs('/home/pi/pihos/usb')
    size = (statvfs.f_frsize * statvfs.f_blocks) / 1073741824.00
    avail = (statvfs.f_frsize * statvfs.f_bavail) / 1073741824.00 
    per = (( size - avail ) / size ) * 100
    print '/home/pi/pihos/usb  Size = {0:.2f} Avail = {1:.2f} Use% = {2:.2f}'.format(size,avail,per)
    
print 'Memmory is < 70 OK!!'
