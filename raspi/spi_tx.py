from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM
import mysql.connector
from threading import Timer, Lock
import signal
import sys
#from sense_hat import SenseHat
from time import sleep
import datetime
import spidev

SPI_BUS = 0
SPI_SS = 0
SPI_CLOCK = 14000000

spi = spidev.SpiDev(SPI_BUS, SPI_SS)
#spi.open(0, 0)
spi.max_speed_hz = SPI_CLOCK

def closeDB(signal, frame):
    print("BYE")
    mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
    cur.close()
    db.close()
    timer.cancel()
    timer2.cancel()
    sys.exit(0)

def polling():
    global cur, db, ready
    
    lock.acquire()
    cur.execute("select * from command order by time desc limit 1")
    for (id, time, cmd_string, arg_string, is_finish) in cur:
        if is_finish == 1 : break
        ready = (cmd_string, arg_string)
        cur.execute("update command set is_finish=1 where is_finish=0")

    db.commit()
    lock.release()
     
    global timer
    timer = Timer(0.1, polling)
    timer.start()

def sensing():
    global cur, db#, sense

    #pressure = sense.get_pressure()
    #temp = sense.get_temperature()
    #humidity = sense.get_humidity()
    pressure = 1
    temp = 1
    humidity = 1
    
    time = datetime.datetime.now()
    num1 = round(pressure / 10000, 3)
    num2 = round(temp / 100, 2)
    num3 = round(humidity / 100, 2)
    meta_string = '0|0|0'
    is_finish = 0

    print(num1, num2, num3)
    query = "insert into sensing(time, num1, num2, num3, meta_string, is_finish) values (%s, %s, %s, %s, %s, %s)"
    value = (time, num1, num2, num3, meta_string, is_finish)

    lock.acquire()
    cur.execute(query, value)
    db.commit()
    lock.release()

    global timer2
    timer2 = Timer(1, sensing)
    timer2.start()

def go():
    spi.open(0, 0)
    tx = [1]
    rx = spi.xfer2(tx) 
    myMotor.setSpeed(70)
    myMotor.run(Raspi_MotorHAT.FORWARD)
    spi.close()

def back():
    spi.open(0, 0)
    tx = [2]
    rx = spi.xfer2(tx)
    myMotor.setSpeed(70)
    myMotor.run(Raspi_MotorHAT.BACKWARD)
    spi.close()

def stop():
    spi.open(0, 0)
    tx = [3]
    rx = spi.xfer2(tx)
    myMotor.setSpeed(70)
    myMotor.run(Raspi_MotorHAT.RELEASE)
    spi.close()

def left():
    spi.open(0, 0)
    tx = [4]
    rx = spi.xfer2(tx)
    pwm.setPWM(0, 0, 280)
    spi.close()

def mid():
    spi.open(0, 0)
    tx = [5]
    rx = spi.xfer2(tx)
    pwm.setPWM(0, 0, 370)
    spi.close()

def right():
    spi.open(0, 0)
    tx = [6]
    rx = spi.xfer2(tx)
    pwm.setPWM(0, 0, 440)
    spi.close()

#init
db = mysql.connector.connect(host='13.209.26.212', user='pgc', password='1234', database='pjtDB', auth_plugin='mysql_native_password')
cur = db.cursor()
ready = None
timer = None

mh = Raspi_MotorHAT(addr=0x6f)
myMotor = mh.getMotor(2)
pwm = PWM(0x6F)
pwm.setPWMFreq(60)

#sense = SenseHat()
timer2 = None
lock = Lock()

signal.signal(signal.SIGINT, closeDB)
polling()
sensing()

#main thread
while True:
    #sleep(0.1)
    if ready == None : continue

    cmd, arg = ready
    ready = None

    if cmd == "go" : go()
    if cmd == "back" : back()
    if cmd == "stop" : stop()
    if cmd == "left" : left()
    if cmd == "mid" : mid()
    if cmd == "right" : right()
spi.close()
