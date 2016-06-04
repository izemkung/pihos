import os
import subprocess

vercurrent = subprocess.check_output('git rev-parse --verify HEAD', shell=True)
print vercurrent

vergit =  os.system('git ls-remote https://github.com/izemkung/pihos | head -1 | cut -f 1')
print vergit

if vergit == vercurrent :
    print "version FW Ok!!!"
    
if vergit != vercurrent :
    print "Download FW "
    os.system('git clone https://github.com/izemkung/pihos /home/pi/tmp && rm -rf /home/pi/pihos && mv /home/pi/tmp/ /home/pi/pihos && rm -rf /home/pi/tmp')
    print "FW Ready to use!!!"