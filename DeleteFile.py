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
import subprocess


if os.path.exists("/home/pi/usb/vdo/ch0") == False:
    os.system('sudo mount /dev/sda1 /home/pi/usb')
    print 'Mount!!!'
    exit()

   
statvfs = os.statvfs('/home/pi/usb')
size = (statvfs.f_frsize * statvfs.f_blocks) / 1073741824.00
avail = (statvfs.f_frsize * statvfs.f_bavail) / 1073741824.00 
per = (( size - avail ) / size ) * 100
print '/home/pi/usb  Size = {0:.2f} Avail = {1:.2f} Use% = {2:.2f}'.format(size,avail,per)

#================================Delet PIC==================================
#print len([name for name in os.listdir('/home/pi/usb/pic/ch0') if os.path.isfile(os.path.join('/home/pi/usb/pic/ch0', name))])
#print min(glob.iglob('/home/pi/usb/pic/ch0/*.[Jj][Pp][Gg]'), key=os.path.getctime)
count = len([name for name in os.listdir('/home/pi/usb/pic/ch0') if os.path.isfile(os.path.join('/home/pi/usb/pic/ch0', name))]) 
numDel = 0 
print 'NUM Pic ch0 {0} '.format(count)
if count > 100: 
    while count > 50: 
        pic0 = min(glob.iglob('/home/pi/usb/pic/ch0/*.[Jj][Pp][Gg]'), key=os.path.getctime)
        count -= 1
        numDel += 1
        #print 'Delete' + pic0
        os.remove(pic0)
    print 'Delete {0} file in /home/pi/usb/pic/ch0/ '.format(numDel)
    
count = len([name for name in os.listdir('/home/pi/usb/pic/ch1') if os.path.isfile(os.path.join('/home/pi/usb/pic/ch1', name))])
numDel = 0
print 'NUM Pic ch1 {0} '.format(count)   
if  count > 100:
    while count > 50:
        pic1 = min(glob.iglob('/home/pi/usb/pic/ch1/*.[Jj][Pp][Gg]'), key=os.path.getctime) 
        count -= 1
        numDel += 1
        #print 'Delete' + pic1
        os.remove(pic1)
    print 'Delete {0} file in /home/pi/usb/pic/ch1/ '.format(numDel)
    
if per < 80 :
    print 'Memmory is < 80% Ok!!'
    time.sleep(60)
    vercurrent = subprocess.check_output('git rev-parse --verify HEAD', shell=True)
    print 'Cur ver ' + vercurrent

    vergit =  subprocess.check_output('git ls-remote https://github.com/izemkung/pihos | head -1 | cut -f 1', shell=True)
    print 'Git ver '+ vergit
    if vergit == vercurrent :
        print "version FW Ok!!!"   
    if vergit != vercurrent :
        print "Download FW "
        print subprocess.check_output('git clone https://github.com/izemkung/pihos /home/pi/tmp', shell=True)
        print subprocess.check_output('rm -rf /home/pi/pihos', shell=True)
        print subprocess.check_output('mv /home/pi/tmp /home/pi/pihos', shell=True)
        #print subprocess.check_output('rm -rf /home/pi/tmp', shell=True)
        print "FW Ready to use!!!"
        os.system('sudo reboot')
        #break
    time.sleep(300)
    #continue
    
while per > 70 :
    OldVideo0 = min(glob.iglob('/home/pi/usb/vdo/ch0/*.[Aa][Vv][Ii]'), key=os.path.getctime)
    OldVideo1 = min(glob.iglob('/home/pi/usb/vdo/ch1/*.[Aa][vv][Ii]'), key=os.path.getctime)

    count = 0
    for file in os.listdir("/home/pi/usb/pic/ch0/"):
        if file.endswith(".jpg"):
            if os.path.getctime("/home/pi/usb/pic/ch0/" + file) < os.path.getctime(OldVideo0) :
                os.remove("/home/pi/usb/pic/ch0/" + file)
                count = count +1

    os.remove(OldVideo0)
    print 'Delete '+ OldVideo0 
    print 'Delete {0} file in /home/pi/usb/pic/ch0/ '.format(count)

    count = 0;
    for file in os.listdir("/home/pi/usb/pic/ch1/"):
        if file.endswith(".jpg"):
            if os.path.getctime("/home/pi/usb/pic/ch1/" + file) < os.path.getctime(OldVideo1) :
                os.remove("/home/pi/usb/pic/ch1/" + file)
                count = count +1
                
    os.remove(OldVideo1)
    print 'Delete '+ OldVideo1       
    print 'Delete {0} file in /home/pi/usb/pic/ch1/ '.format(count)

    statvfs = os.statvfs('/home/pi/usb')
    size = (statvfs.f_frsize * statvfs.f_blocks) / 1073741824.00
    avail = (statvfs.f_frsize * statvfs.f_bavail) / 1073741824.00 
    per = (( size - avail ) / size ) * 100
    print '/home/pi/usb  Size = {0:.2f} Avail = {1:.2f} Use% = {2:.2f}'.format(size,avail,per)
    
print 'Memmory is < 70 OK!!!'
#print 'Memmory is Error'
