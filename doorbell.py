import RPi.GPIO as GPIO
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.utils import COMMASPACE, formatdate
from email import encoders
import feedparser
import uuid
import os
from picamera import PiCamera

def email(string,gmail,count):
	USERNAME = "pvg.raspberry@gmail.com"
	PASSWORD = "raspberrypi"
	#MAILTO = "shreemay1993@gmail.com"
	MAILTO = gmail
	#msg = MIMEText('Someone is at your door')
	msg = MIMEMultipart()
	msg['Subject'] = string
	msg['From'] = USERNAME
	msg['To'] = MAILTO
	msg.attach(MIMEText("Hello, this person is at your door."))
	filename = str(count) + '.jpg'
	attachment = open(str(count) + '.jpg','rb')
	fp = open(str(count) + '.jpg', 'rb')
	img = MIMEImage(fp.read())
	fp.close()
	msg.attach(img)
	'''
	part = MIMEBase('application','octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition',"attachment; filename=%s" % filename)
	msg.attach(part)
	'''
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo_or_helo_if_needed()
	server.starttls()
	server.ehlo_or_helo_if_needed()
	server.login(USERNAME,PASSWORD)
	server.sendmail(USERNAME,MAILTO,msg.as_string())
	server.quit()
	print "The mail has been sent to " + gmail

def display(string):
	USERNAME = "pvg.raspberry@gmail.com"
	PASSWORD = "raspberrypi"
	response = feedparser.parse("https://" + USERNAME + ":" + PASSWORD + "@mail.google.com/gmail/feed/atom")
	unread_count = int(response["feed"]["fullcount"])
	if string in response['items'][0].title and unread_count > 0:
		os.system('clear')
		print response['items'][0].description
		return 1
	return 0
def capture(count):
	camera = PiCamera()
	camera.start_preview()
	camera.capture(str(count) + '.jpg')
	camera.stop_preview()
	camera.close()

GPIO.setmode(GPIO.BCM)

GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#string = 0
flag = 0
count = 0
while True:
    input_state = GPIO.input(18)
    if input_state == False:
        print('Button Pressed')
        string = str(uuid.uuid1())
        count += 1
	capture(count)
        email(string,'shreemay1993@gmail.com',count)
	email(string,'ketakic1990@gmail.com',count)
	email(string,'akshatvaidya1@gmail.com',count)
        stored_string = string
    while input_state == False:
        input_state = GPIO.input(18)
    '''
    if string != 0:
        flag = display(string)
        if flag == 1:
            time.sleep(5)
            os.system('clear')
            print("WELCOME")
            string = 0
    '''