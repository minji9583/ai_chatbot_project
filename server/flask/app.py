import pickle
from scipy.sparse import lil_matrix
from konlpy.tag import Okt

import numpy as np

from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

with open('model.clf', 'rb') as f:
    model = pickle.load(f)

word_indices = model.get_word_indices()
naive = model.get_naive_model()
logi = model.get_logistic_model()
knn = model.get_k_neighbors_model()


okt = Okt()


def tokenize(doc):
    tt = okt.pos(doc, norm=True, stem=True)
    return ['/'.join(t) for t in tt]


def preprocess(text):
    vocas = tokenize(text)
    X = [0] * (len(word_indices) + 1)
    for voca in vocas:
        indices = word_indices.get(voca)
        if indices:
            X[indices] = 1
    X = [X]
    return np.array(X)

def classify(text):
    data = preprocess(text)
    result1 = naive.predict(data)[0]
    result2 = logi.predict(data)[0]
    result3 = knn.predict(data)[0]

    if result1 + result2 + result3 >= 2:
        return "긍정"
    else:
        return "부정"


class Data(Resource):
    def get(self, text):
        ans = classify(text)
        return {'result': ans}


api.add_resource(Data, '/<string:text>')

if __name__ == '__main__':
    app.debug = True
    app.run()