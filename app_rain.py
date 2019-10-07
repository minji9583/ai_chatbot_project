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
from flask import request
import json
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
    return pred.predict(text)
    
# Req 2-2-2. app.db 를 연동하여 웹에서 주고받는 데이터를 DB로 저장
    

# 챗봇이 멘션을 받았을 경우
@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    print(event_data)
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
        print(text)
        reply = predict(text)
        slack_web_client.chat_postMessage(
            channel=channel,
            text=reply,
            attachments=[
                {
                    "text": "잘못된 답변이면 신고 버튼을 클릭해주세요",
                    "fallback": "신고 버튼을 누르지 않았어요",
                    "callback_id": "report_message",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                        {
                            "name": "report",
                            "text": "신고",
                            "style": "danger",
                            "type": "button",
                            "value": text,
                            "confirm": {
                                "title": "신고 하시겠습니까?",
                                "text": "최선입니까? 확실해요?",
                                "ok_text": "네",
                                "dismiss_text": "아니오"
                            }
                        }
                    ]
                }
            ]
        )

def on_json_loading_failed_return_dict(e):
    return {}


@app.route("/post", methods=['POST'])
def test():
    print("안녕", request.form)
    req = request.form['payload']
    json_req = json.loads(req)
    print("req", json_req)
    # print("actions", json_req['actions'])
    # print("value", json_req['actions'][0]['value'])
    value = json_req['actions'][0]['value']
    insert(value)
    return "신고 접수가 되었습니다!"



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

@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run()
