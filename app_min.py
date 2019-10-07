import data
import model as ml
import predict_min as pred
import tensorflow as tf
import sqlite3

import os
import json
import pickle
import numpy as np

from flask import g
from threading import Thread
from configs import DEFINES
from flask import Flask, request
from flask_restful import reqparse
from slack import WebClient
from slackeventsapi import SlackEventAdapter

# slack 연동 정보 입력 부분
SLACK_TOKEN = 'xoxb-718907786578-720177174562-1qx9BjbVbLkrIB9yfikj8fVr'
SLACK_SIGNING_SECRET = 'fa3d6193e36d26163abc90a4507ceec8'

app = Flask(__name__)

slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

return_text = ""
time_stamp = 0


# Req. 2-2-1 대답 예측 함수 구현
def predict(text):
    return pred.predict(text)

# Req 2-2-2. app.db 를 연동하여 웹에서 주고받는 데이터를 DB로 저장
def insert(text):
    # app.db 파일을 연결
    conn = sqlite3.connect('app.db')
    # 사용할 수 있도록 설정(?)
    c = conn.cursor()
    # 쿼리문
    c.execute('INSERT INTO search_history(query) VALUES(?)', (text,))
    # 저장
    conn.commit()
    # app.db 파일 연결 해제
    conn.close()

# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    global return_text, time_stamp
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]
    ts = float(event_data["event"]["ts"])
    text = ' '.join(text.split('>')[1:])
    if text[0] == " ":
        text = text[1:]
    if ts > time_stamp:
        time_stamp = ts
        return_text = text
        reply = predict(text)
        slack_web_client.chat_postMessage(
            channel=channel,
            text=reply,
            attachments=
            [
                {
                    "text" : "답변이 마음에 들지 않으면 `🚫 신고하기 🚫`를 눌러주세요.",
                    "fallback": "마음에 들지 않는 답변에 대한 질문 수집",
                    "callback_id": "report_msg",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                        {
                            "name": "report",
                            "text": "🚫 신고하기 🚫",
                            "style": "danger",
                            "type": "button",
                            "value": text,
                        }
                    ]
                }
            ]
        )

@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"

@app.route("/post", methods=["POST"])
def post():
    req = request.form['payload']
    json_req = json.loads(req)
    value = json_req['actions'][0]['value']
    insert(value)

    return "접수완료"

if __name__ == '__main__':
    app.run()
