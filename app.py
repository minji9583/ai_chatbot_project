import data
import model as ml
import predict as pred
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
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')

app = Flask(__name__)

slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

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
    text = ' '.join(event_data["event"]["text"].split('>')[1:])
    if text[0] == " ":
        text = text[1:]
    ts = float(event_data["event"]["ts"])
    # print(ts)

    if ts > time_stamp:
        time_stamp = ts
        # print(text)
        reply = predict(text)
        # print(reply)
        slack_web_client.chat_postMessage(
            channel=channel,
            text=reply,
            attachments=[
                {
                    "text": "잘못된 답변이면 `🚫 신고하기 🚫` 버튼을 클릭해주세요",
                    "fallback": "신고 버튼을 누르지 않았어요",
                    "callback_id": "report_message",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                        {
                            "name": "report",
                            "text": "🚫 신고하기 🚫",
                            "style": "danger",
                            "type": "button",
                            "value": text,
                            "confirm": {
                                "title": "신고",
                                "text": "진짜 신고 하시겠습니까?",
                                "ok_text": "네",
                                "dismiss_text": "아니오"
                            }
                        }
                    ]
                }
            ]
        )


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"

@app.route("/report", methods=["POST"])
def save_text():
    req = json.loads(request.form["payload"])
    return f"질문 '{req.get('actions')[0]['value']}'에 대한 답변 '{req['original_message']['text']}'신고 완료"

if __name__ == '__main__':
    app.run()
