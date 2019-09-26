import data
import model as ml
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
SLACK_TOKEN = "xoxb-718907786578-720177174562-oKkmHrXJhhDyxatiVMO3A9pK"
SLACK_SIGNING_SECRET = "fa3d6193e36d26163abc90a4507ceec8"

app = Flask(__name__)

slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


# Req. 2-2-1 대답 예측 함수 구현
def predict():

    return None

# Req 2-2-2. app.db 를 연동하여 웹에서 주고받는 데이터를 DB로 저장
def insert(text):
    # app.db 파일을 연결
    conn = sqlite3.connect('app.db')
    # 사용할 수 있도록(?) 설정
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
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run()
