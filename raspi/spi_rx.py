from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM
import spidev

SPI_BUS = 0          # spidev0
SPI_SS  = 0          # spidev0.0
SPI_CLOCK = 14000000  # 1 Mhz

# setup SPI
spi = spidev.SpiDev(SPI_BUS, SPI_SS)
spi.open(0,0)
spi.max_speed_hz = SPI_CLOCK
tx = [0]

def go():
    #print("go")
    myMotor.setSpeed(100)
    myMotor.run(Raspi_MotorHAT.FORWARD)
    spi.close()
    spi.open(0, 0)

def back():
    #print("back")
    myMotor.setSpeed(100)
    myMotor.run(Raspi_MotorHAT.BACKWARD)
    spi.close()
    spi.open(0, 0)

def stop():
    #print("stop")
    myMotor.setSpeed(100)
    myMotor.run(Raspi_MotorHAT.RELEASE)
    spi.close()
    spi.open(0, 0)

def left():
    #print("left")
    pwm.setPWM(0, 0, 280)
    spi.close()
    spi.open(0, 0)

def mid():
    #print("mid")
    pwm.setPWM(0, 0, 370)
    spi.close()
    spi.open(0, 0)

def right():
    #print("right")
    pwm.setPWM(0, 0, 440)
    spi.close()
    spi.open(0, 0)

mh = Raspi_MotorHAT(addr=0x6f)
myMotor = mh.getMotor(2)
pwm = PWM(0x6F)
pwm.setPWMFreq(60)

while True:
    try:
        rx = spi.xfer2(tx)
        if rx == [1] : go()
        elif rx == [2] : back()
        elif rx == [3] : stop()
        elif rx == [4] : left()
        elif rx == [5] : mid()
        elif rx == [6] : right()
        else : pass
    except spi.SPIException:
        pass
