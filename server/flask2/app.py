# -- coding: utf-8 --
import pickle
from scipy.sparse import lil_matrix
from konlpy.tag import Okt
import json
import numpy as np
from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


class Data(Resource):
    def get(self, text):
        ans = text
        return {"result": ans}

parser.add_argument('payload')

class Db(Resource):
    def post(self):
        args = parser.parse_args().payload
        args = json.loads(args)
        text = args['actions'][0]['value']
        with open('report.csv', 'a', encoding='utf-8') as f:
            f.write(text+',\n')
        return make_response('접수되었습니다.')

api.add_resource(Data, '/<string:text>')
api.add_resource(Db, '/db')

if __name__ == '__main__':
    app.debug = True
    app.run()