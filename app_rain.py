import data
import model as ml
import predict_rain as pred
import tensorflow as tf
import sqlite3

import os
import pickle
import numpy as np

from flask import g
from threading import Thread
from configs import DEFINES
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter


# slack 연동 정보 입력 부분
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')

app = Flask(__name__)

slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

return_text = ""
time_stamp = 0

# Req. 2-2-1 대답 예측 함수 구현
def predict(text):
    text = ' '.join(text.split('>')[1:])
    return pred.predict(text)
    
# Req 2-2-2. app.db 를 연동하여 웹에서 주고받는 데이터를 DB로 저장
    

# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    global return_text, time_stamp
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]
    ts = float(event_data["event"]["ts"])
    print(ts)
    if ts > time_stamp:
        time_stamp = ts
        print(text)
        reply = predict(text)
        print(reply)
        slack_web_client.chat_postMessage(
            channel=channel,
            text=reply
        )

@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run()
