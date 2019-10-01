import tensorflow as tf
import model as ml
import data_ming as data
import numpy as np
import os
import sys
import pickle

from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction
from rouge import Rouge

from configs import DEFINES

DATA_OUT_PATH = './data_out/'


# Req. 1-5-1. bleu score 계산 함수

def bleu_compute(ture, val):
    smooth = SmoothingFunction().method2
    score = sentence_bleu(
        [ture.split()],
        val.split(),
        weights=(0.25, 0.25, 0.25, 0.25),
        smoothing_function=smooth)

    return score


# Req. 1-5-2. rouge score 계산 함수
def rouge_compute(answer, pred):
    rouge = Rouge()
    scores = rouge.get_scores(answer, pred)
    score1 = scores[0]['rouge-1']
    return score1['r'], score1['p'], score1['f']


# Req. 1-5-3. main 함수 구성
def main(self):
    data_out_path = os.path.join(os.getcwd(), DATA_OUT_PATH)
    os.makedirs(data_out_path, exist_ok=True)
    # 데이터를 통한 사전 구성 한다.
    char2idx, idx2char, vocabulary_length = data.load_voc()
    # 훈련 데이터와 테스트 데이터를 가져온다.

    train_q, train_a, test_q, test_a = data.load_data()
    # print('train_q', train_q)
    # print('train_a', train_a)
    # print('test_q', test_q)
    # print('test_a', test_a)

    # 훈련셋 인코딩 만드는 부분
    train_input_enc = data.enc_processing(train_q, char2idx)
    # print('train_input_enc', train_input_enc)
    # 훈련셋 디코딩 입력 부분
    train_input_dec = data.dec_input_processing(train_a, char2idx)
    # print('train_input_dec', train_input_dec)
    # 훈련셋 디코딩 출력 부분
    train_target_dec = data.dec_target_processing(train_a, char2idx)
    print('train_target_dec', train_target_dec)

    # 평가셋 인코딩 만드는 부분
    eval_input_enc = data.enc_processing(test_q, char2idx)
    # 평가셋 인코딩 만드는 부분
    eval_input_dec = data.dec_input_processing(test_a, char2idx)
    # 평가셋 인코딩 만드는 부분
    eval_target_dec = data.dec_target_processing(test_a, char2idx)

    # 현재 경로'./'에 현재 경로 하부에
    # 체크 포인트를 저장한 디렉토리를 설정한다.
    check_point_path = os.path.join(os.getcwd(), DEFINES.check_point_path)
    # 디렉토리를 만드는 함수이며 두번째 인자 exist_ok가
    # True이면 디렉토리가 이미 존재해도 OSError가
    # 발생하지 않는다.
    # exist_ok가 False이면 이미 존재하면
    # OSError가 발생한다.
    os.makedirs(check_point_path, exist_ok=True)
    # 에스티메이터 구성한다.

    classifier = tf.estimator.Estimator(
        model_fn=ml.model,  # 모델 등록한다.
        model_dir=DEFINES.check_point_path,  # 체크포인트 위치 등록한다.
        params={  # 모델 쪽으로 파라메터 전달한다.
            'embedding': DEFINES.embedding,
            'hidden_size': DEFINES.hidden_size,  # 가중치 크기 설정한다.
            # 'ffn_hidden_size': DEFINES.ffn_hidden_size,
            # 'attention_head_size': DEFINES.attention_head_size,
            'learning_rate': DEFINES.learning_rate,  # 학습율 설정한다.
            'vocabulary_length': vocabulary_length,  # 딕셔너리 크기를 설정한다.
            'embedding_size': DEFINES.embedding_size,  # 임베딩 크기를 설정한다.
            'layer_size': DEFINES.layer_size,
            'max_sequence_length': DEFINES.max_sequence_length,
            'multilayer': DEFINES.multilayer,  # 멀티 레이어 사용 유무를 설정한다.
            # 'xavier_initializer': DEFINES.xavier_initializer

        })

    # 학습 실행
    classifier.train(input_fn=lambda: data.train_input_fn(
        train_input_enc, train_input_dec, train_target_dec, DEFINES.batch_size), steps=DEFINES.train_steps)
    eval_result = classifier.evaluate(input_fn=lambda: data.eval_input_fn(
        eval_input_enc, eval_input_dec, eval_target_dec, DEFINES.batch_size))

    print('\nEVAL set accuracy: {accuracy:0.3f}\n'.format(**eval_result))

    # 모델 저장
    with open("model.clf", "wb") as f:
        pickle.dump(classifier, f)

    # 테스트용 데이터 만드는 부분이다.
    # 인코딩 부분 만든다. 테스트용으로 ["가끔 궁금해"] 값을 넣어 형성된 대답과 비교를 한다.
    predic_input_enc = data.enc_processing(["가끔 궁금해"], char2idx)
    # 학습 과정이 아니므로 디코딩 입력은
    # 존재하지 않는다.(구조를 맞추기 위해 넣는다.)
    predic_input_dec = data.dec_input_processing([""], char2idx)
    # 학습 과정이 아니므로 디코딩 출력 부분도
    # 존재하지 않는다.(구조를 맞추기 위해 넣는다.)
    predic_target_dec = data.dec_target_processing([""], char2idx)
    print('predic_input_enc', predic_input_enc)
    print('predic_input_dec', predic_input_dec)
    print('predic_target_dec', predic_target_dec)

    # with open("model.clf", "rb") as f:
    #     classifier = pickle.load(f)

    predictions = classifier.predict(
        input_fn=lambda: data.eval_input_fn(predic_input_enc, predic_input_dec, predic_target_dec, 1))
    # print('predictions', predictions)
    answer, finished = data.pred_next_string(predictions, idx2char)
    # print('answer, finished', answer, finished)k

    # 예측한 값을 인지 할 수 있도록
    # 텍스트로 변경하는 부분이다.

    print("answer: ", answer)
    print("Bleu score: ", bleu_compute("안녕하세요", answer))
    print("Rouge score: ", rouge_compute("안녕하세요", answer))


if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)

tf.logging.set_verbosity
