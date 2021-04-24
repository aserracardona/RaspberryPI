#!/home/pi/jupyter-env/bin/python3

import os
import time
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO

camera = PiCamera()

camera.led = False

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN) #GPIO pin where the PIR sensor is connected

bot = telepot.Bot('123456789:telegrambottoken') #Telegram bot token

chat_id = 123456789 #Chat ID of the group chat with the bot

time.sleep(5)

bot.getMe()

camera.led = False


def motion_alert():
    print('Motion detected!')
    intruder_time = 'Motion Alert! ' + time.strftime("%Y/%m/%d %H:%M:%S")
    bot.sendMessage(chat_id, intruder_time)
    take_pic()
    time.sleep(60) #time before the motion detector will be activated again

def take_pic():
    camera.start_preview()
    camera.annotate_text_size = 12
    camera.annotate_text = time.strftime("%Y/%m/%d %H:%M:%S")
    sleep(2) #it's important to sleep for at leas 2 sec before taking picture to let the sensor adjust
    camera.capture('/home/pi/Pictures/PiCamera/image.jpg',use_video_port=True) #directory where the picture is saved
    camera.stop_preview() 
    bot.sendPhoto(chat_id, open('/home/pi/Pictures/PiCamera/image.jpg', 'rb')) #sends the picture it just took
    
def PIR_control_ON():
    global PIR_status
    PIR_status = True
    bot.sendMessage(chat_id, 'PIR Camera ON')
    
def PIR_control_OFF():
    global PIR_status
    PIR_status = False
    bot.sendMessage(chat_id, 'PIR Camera OFF')

def reboot():
    bot.sendMessage(chat_id, 'Rebooting')
    os.system('sudo reboot')    
    
telegram_func = {
    'Take picture' : take_pic,
    'Turn PIR Camera ON' : PIR_control_ON,
    'Turn PIR Camera OFF' : PIR_control_OFF,
    'Reboot' : reboot,
}

PIR_status = True

offset_value = 0

time.sleep(5)

bot.sendMessage(chat_id, 'ONLINE')
    
while True:
    
    if PIR_status:
        if GPIO.input(17):
            motion_alert()
    
    response = bot.getUpdates(offset=offset_value)
                              
    if response:                          
    
        keyboard=ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Take picture")],
            [KeyboardButton(text='Turn PIR Camera ON')],
            [KeyboardButton(text='Turn PIR Camera OFF')],
            [KeyboardButton(text='Reboot')]
            ], one_time_keyboard=True) 

        bot.sendMessage(chat_id, 'Choose an option:', reply_markup=keyboard)

        response = bot.getUpdates(offset=offset_value)
    
        offset_value = response[-1]['update_id'] + 1
        
        if response[-1]['message']['text'] in telegram_func:
            telegram_func[response[-1]['message']['text']]()
