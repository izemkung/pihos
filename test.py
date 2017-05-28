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

#===================================================Update FW Version================================
vercurrent = subprocess.check_output('sudo rm /home/pi/usb/pic/ch0/*.jpg', shell=True)
print vercurrent
if vercurrent == '' :
    print 'isOK' + vercurrent
if vercurrent == 'No such file or directory' :
    print ' No such 5555555'
