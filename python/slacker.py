#!/usr/bin/python

import re
import time
import json
from slackclient import SlackClient

# when i have time, instead slack_client will read from ../secrets/slack.key
slack_client = SlackClient("hint, don't publish your slack api key")

user_list = slack_client.api_call("users.list")
for user in user_list.get('members'):
    if user.get('name') == "gohan-time":
        slack_user_id = user.get('id')
        break

if slack_client.rtm_connect():
    print "Connected!"

    while True:
        for message in slack_client.rtm_read():
            if 'text' in message and message['text'].startswith("<@%s>" % slack_user_id):

                print "Message received: %s" % json.dumps(message, indent=2)

                message_text = message['text'].\
                        split("<@$s>" % slack_user_id)[1].\
                        strip()

                if message_text:
                    slack_client.api_call(
                       "chat.postMessage",
                       channel=message['channel'],
                       text="Oh?",
                       as_user=True)
    time.sleep(1)
                

