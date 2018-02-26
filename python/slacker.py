#!/usr/bin/python

import re
import time
import json
from slackclient import SlackClient

slack_client = SlackClient("xoxb-320650244449-2LPv18JyV3zRWiDLru61wwMS")

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

                if re.match(r'.*(yum).*', message_text, re.IGNORECASE):
                    reply = "There is food"

                    slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text="Oh? %s" % reply,
                            as_user=True)
    time.sleep(1)
                

