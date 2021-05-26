#Motor control using flex sensor and fsr sensor
import time
import spidev
import RPi.GPIO as GPIO

spi=spidev.SpiDev()
spi.open(0, 0) #0ch
spi.max_speed_hz=1000000

pin1 = 18 #first motor pin number
pin2 = 23 #second motor pin number
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #gpio pin number
GPIO.setup(pin1, GPIO.OUT) #set to out
GPIO.setup(pin2, GPIO.OUT) #set to out
p1= GPIO.PWM(pin1, 50)  #PMW
p2= GPIO.PWM(pin2, 50)  #PMW
p1.start(0)
p2.start(0)

motor_min=1   #servo value min
motor_max=13  #servo value max

def ReadVol(vol):
    adc=spi.xfer2([1,(8+vol)<<4,0])
    data=((adc[1]&3)<<8)+adc[2]
    return data

def resistor_1(flex1):  #0ch - change flex value to servo value
    flex_min=110 #flex value min
    flex_max=460 #flex value max
    #new servo value
    servo_v = ((flex1-flex_min)/(flex_max-flex_min))*(motor_max-motor_min)+motor_min
    return servo_v

def resistor_2(flex2):  #1ch - change flex value to servo value
    flex_min=50 #flex value min
    flex_max=280 #flex value max
    #new servo value
    servo_v = ((flex2-flex_min)/(flex_max-flex_min))*(motor_max-motor_min)+motor_min
    return servo_v

mcp3008=0   #0ch
mcp3008_1=1 #1ch
mcp3008_2=2 #2ch

try:
    while True:
        flex1 = ReadVol(mcp3008)   #first flex
        flex2 = ReadVol(mcp3008_1) #second flex
        fsr = ReadVol(mcp3008_2)   #pressure sensor
        p1.ChangeDutyCycle(resistor_1(flex1))  #first servo value 
        p2.ChangeDutyCycle(resistor_2(flex2))  #second servo value
        print('flex1: ', flex1)
        print('flex2: ', flex2)
        print('fsr: ', fsr)
        print('servo1: ', resistor_1(flex1))
        print('servo2: ', resistor_2(flex2))
        time.sleep(0.15)
        while fsr>50:  #if the pressure value is over 50, it stop
            fsr = ReadVol(mcp3008_2) #check pressure values after stopping
            p1.ChangeDutyCycle(0) #first motor stop
            p2.ChangeDutyCycle(0) #second motor stop

        
except KeybordInterrupt:
     p.stop()

GPIO.cleanup()



