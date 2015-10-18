import urllib2
import time
import os
from bs4 import BeautifulSoup

IP = '10.5.5.9'
API_URL = 'http://' + IP
WEB_URL = 'http://' + IP + ':8080'
CAPTURE_LIST = WEB_URL + '/videos/DCIM/100GOPRO/'

PASSWORD = 'conectar'

def power_off():
    """Turn camera off """
    print
    print power_off.__doc__
    command_send('bacpac', 'PW', '00')

def power_on():
    """Turn camera on """
    print
    print power_on.__doc__
    command_send('bacpac', 'PW', '01')

def capture_start():
    """Start a capture """
    print
    print capture_start.__doc__
    command_send('bacpac', 'SH', '01')

def mode_photo():
    """Switch to photo mode """
    print
    print mode_photo.__doc__
    command_send('camera', 'CM', '01')

def delete_all():
    """Delete all captures
    This will delete all of the media on the camera. """
    print
    print delete_last.__doc__
    command_send('camera', 'DA', '')

def last_capture():
    """Get the most recent capture
    It's probably worth checking this a bit.
    The last item in the list might not be the latest.
    Best to check for the largest number.
    Do these loop over to the begining?
    """
    capture_files = list_captures()
    #print 'File: %s' % capture_files[-1]
    return capture_files[-1]

def list_captures():
    """Get a list of the videos and photo files on the GoPro
    Use BeautifulSoup to parse the GoPro's list of captures
    This list of captures is provided by the Cherokee webserver on the GoPro
    To get this capture the GoPro Hero 3 Black
    """
    page = urllib2.urlopen(CAPTURE_LIST)
    html_page = page.read()
    soup = BeautifulSoup(html_page)
    captures = soup.find_all('a', class_='link')
    capture_files = []
    for capture in captures:
        capture_file = capture.get('href')
        capture_files.append(capture_file)
    return capture_files

def main():

   lapse = True

   while lapse:
       power_on()
       time.sleep(7)
       mode_photo()
       time.sleep(4)
       capture_start()
       time.sleep(5)
       os.system("wget http://10.5.5.9:8080/videos/DCIM/100GOPRO/"+last_capture()+"")
       delete_all()
       time.sleep(5)
       power_off()
       time.sleep(450)

if __name__ == "__main__":
    main()