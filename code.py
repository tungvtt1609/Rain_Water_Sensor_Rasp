import telepot
import RPi.GPIO as GPIO
import time
import datetime
from telepot.loop import MessageLoop
from time import sleep

rain = 18
servo = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(rain, GPIO.IN)
GPIO.setup(11, GPIO.OUTPUT)

motion = 0
motionNew = 0

servo1 = GPIO.PWM(11, 50)
servo1.start(0)
time.sleep(2)
duty = 2

def handle(msg):
    global telegramText
    global chat_id 

    chat_id = msg['chat']['id']
    telegramText = msg['text']

    print('Message received from' + str(chat_id))

    if telegramText == '/start':
        bot.sendMessage(chat_id, 'Welcome to Smart Home')
    
    while True:
        main()


bot = telepot.Bot('5452453117:AAGgOPQ5cK30rSSOFUo05E72Os08pLh6hok')
bot.message_loop(handle)

def main():
    global chat_id
    global motion
    global motionNew

    if GPIO.input(rain):
        print("Rain detected")
        motion = 0
        if motionNew != motion:
            motionNew = motion
            sendNotification(motion)
            ser(motion)
            
    else:
        print("No Rain detected")
        motion = 1
        if motionNew != motion:
            motionNew = motion
            ser(motion)

def ser(motion):
    global chat_id
    if motion == 0:
        while duty <= 12:
            servo1.ChangeDutyCycle(duty)
            time.sleep(1)
            duty = duty + 1
        time.sleep(1)

    else:
        servo1.ChangeDutyCycle(7)
        time.sleep(2)

        servo1.ChangeDutyCycle(2)
        time.sleep(0.5)

        servo1.ChangeDutyCycle(0)

    servo1.stop()
    GPIO.cleanup()


def sendNotification(motion):
    global chat_id
    if motion == 1:
        bot.sendMessage(chat_id, 'It is raining')
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    else:
        bot.sendMessage(chat_id, 'No rain')
        bot.sendMessage(chat_id, str(datetime.datetime.now()))

while True:
    time.sleep(10)