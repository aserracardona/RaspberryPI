# Python script to communicate with a motion-activated Raspberry Pi Camera using a Telegram bot

This script will allow you to control a Raspberry Pi Camera with a passive infrared (PIR) motion sensor from your phone.

By chatting with the Telegram bot you can:

  - Recieve an alert everytime the motion sensor gets activated as well as the picture
  - Take a picture with the Raspberry Pi Camera
  - Turn the motion sensor on or off
  - Reboot the Raspberry Pi


<img src="https://github.com/aserracardona/RaspberryPI/blob/main/MotionCam/Screenshot.jpg" alt="drawing" width="300"/>


## Requirements
It requires [telepot](https://telepot.readthedocs.io/en/latest/#) to interact with the Telegram bot.

You will need to create a [Telegram bot](https://core.telegram.org/bots) and add it into a group chat.

In the script, you will need to add the bot token and the chat id in the indicated variables (refer to [here](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id) to obtain the chat id).
