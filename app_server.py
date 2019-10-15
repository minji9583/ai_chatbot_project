# -- coding: utf-8 --
import pickle
from scipy.sparse import lil_matrix
from konlpy.tag import Okt
import json
import numpy as np
from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
​
import predict as pred
​
​
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
​
cors = CORS(app, resources={
  r"*": {"origin": "*"},
})
​
​
​
class Data(Resource):
    def get(self, text):
        ans = pred.doPredict2(text)
        res = str({"result":ans})
        res = res.replace("\'", "\"")
        return make_response(res)
​
parser.add_argument('payload')
​
class Db(Resource):
    def post(self):
        args = parser.parse_args().payload
        args = json.loads(args)
        text = args['actions'][0]['value']
        with open('report.csv', 'a', encoding='utf-8') as f:
            f.write(text+',\n')
        return make_response('접수되었습니다.')
​
parser.add_argument('siren')
​
class Db2(Resource):
    def post(self):
        args = parser.parse_args().siren
        args = args.replace("\'", "\"")
        args = json.loads(args)
        text = args['result']
        with open('report.csv', 'a', encoding='utf-8') as f:
            f.write(text+',\n')
        return make_response('접수되었습니다.')
​
​
api.add_resource(Db, '/db')
api.add_resource(Db2, '/db2')
api.add_resource(Data, '/chat/<string:text>')
​
if __name__ == '__main__':
    app.run(host="172.26.4.30",port=5000)