#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
import re
import requests
import atexit
import RPi.GPIO as GPIO
from slackclient import SlackClient
from picamera import PiCamera

# Set LED Pinouts

green = 18
red = 23
button = 17

# Set some GPIO stuff
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initial states for LEDs
GPIO.output(green, GPIO.HIGH)
GPIO.output(red, GPIO.LOW)

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
starterbot_id = None

# Slack constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
token = os.environ.get('SLACK_API_TOKEN')

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. To share food, type *yum*. To see what's on camera now, type *hungry*."

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith('yum'):
        response = share_noms()
    elif command.startswith('hungry'):
        response = see_noms()


    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

def share_noms():
    """
    Takes a pic and shares it with #random
    TODO: Ask the user for some input, like "yum Delicious off-brand cola in the breakroom!" i guess?
    """
    message = "How kind of you to share!"
    take_picture()
    post_image()
    return(message)
def see_noms():
    """
    Just takes a photo of whatever is there and kicks it out
    """
    message = "美味しいものなの?"
    return(message)

def take_picture():
    camera = PiCamera()
    camera.resolution = (1920, 1080)
    camera.start_preview()
    time.sleep(2)
    camera.capture('/home/april/gohan-time/images/oishii.jpg')
    camera.close()

def hook_post_image():
    url = 'https://hooks.slack.com/services/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'
    payload = '{"attachments": [{"fallback": "A picture of some food.", "text": "Delicious text.", "image_url": "https://i.redditmedia.com/FjGhVX9geusqgdBvBpi9C3UEcwOUOzaWZxTXXZX3o7I.jpg?w=768&s=95554cd6ab85522aa5507c221ea6a912"}]}'
    requests.request("POST", url, data=payload)

def post_image():
    tasty_treat = {
            'file' : ('/home/april/gohan-time/images/oishii.jpg', open('/home/april/gohan-time/images/oishii.jpg', 'rb'), 'jpg')
            }
    payload={
            "filename":"oishii.jpg",
            "token":token,
            "channels":['#griz_test_chan'],
            }
    r = requests.post("https://slack.com/api/files.upload", params=payload, files=tasty_treat)

def cleanup():
    GPIO.cleanup()
    print("Goodbye!")

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

atexit.register(cleanup)
