#!/usr/bin/python

import os
from slackclient import SlackClient

slack_token = os.environ["SLACK_BOT_TOKEN"]

sc = SlackClient(slack_token)

sc.api_call(
        "chat.postMessage",
        channel="#random",
        text="Testing!"
        )

