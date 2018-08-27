import RPi.GPIO as GPIO
import BlynkLib
import time

from time import sleep

BLYNK_AUTH = 'd2132438bc5244949d13241150f57958'


blynk = BlynkLib.Blynk(BLYNK_AUTH)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(03, GPIO.OUT)
pwm=GPIO.PWM(03, 50)

@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value):
	print('Current V! value: {}'.format(value))
	pwm.start(0)
	print('Value - ')
	print(value)
	if(value == '0'):
		#pwm.start(7)	
		setAngle(54)
		#pwm.stop()
		print('A')
	else:
		#pwm.start(90)
		setAngle(144)
		print('B')


@blynk.VIRTUAL_READ(2)
def my_read_handler():
	blynk.virtual_write(2, time.ticks_ms() // 1000)
	pwm.stop()
	GPIO.cleanup()



def setAngle(angle):
        
	duty = angle /18 +2
	GPIO.output(03, True)
        pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(03, False)
	pwm.ChangeDutyCycle(0)
        


blynk.run()




