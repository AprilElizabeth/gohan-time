#!/bin/bash

export SLACK_BOT_TOKEN=$(cat /home/april/gohan-time/secrets/slack.key)
export SLACK_API_TOKEN=$(cat /home/april/gohan-time/secrets/slack.token)
echo "Starting slacker with "$SLACK_BOT_TOKEN
python /home/april/gohan-time/python/slackerex.py
