from konlpy.tag import Kkma
import pandas as pd
import tensorflow as tf
import enum
import os
import re
from sklearn.model_selection import train_test_split
import numpy as np
from configs import DEFINES


PAD = "<PAD>"
STD = "<SOS>"
END = "<END>"
UNK = "<UNK>"

PAD_INDEX = 0
STD_INDEX = 1
END_INDEX = 2
UNK_INDEX = 3

MARKER = [PAD, STD, END, UNK]


# Req 1-1-1. 데이터를 읽고 트레이닝 셋과 테스트 셋으로 분리
def load_data():
    data_df = pd.read_csv(DEFINES.data_path)
    Q, A = list(data_df['Q']), list(data_df['A'])
    train_q, test_q, train_a, test_a = train_test_split(Q, A)
    return train_q, train_a, test_q, test_a


# Req 1-1-2. 텍스트 데이터에 정규화를 사용하여 ([~.,!?\"':;)(]) 제거
def prepro_noise_canceling(data):
    check = ["~", ".", ",", "!", "?", '"', "'", ":", ";"]
    for line in range(len(data)):
        for i in check:
            if i in data[line]:
                data[line] = data[line].replace(i, "")

    return data

# Req 1-1-3. 텍스트 데이터에 토크나이징
def tokenizing_data(data):
    token_data = data.split()
    return token_data

# Req 1-2-1. 토큰화된 트레이닝 데이터를 인코더에 활용할 수 있도록 전 처리
def enc_processing(value, dictionary):

    # 인덱스 정보를 저장할 배열 초기화
    seq_input_index = []
    # 문장의 길이를 저장할 배열 초기화
    seq_len = []
    # 노이즈 캔슬
    n_value = prepro_noise_canceling(value)
    for seq in n_value:
        # 하나의 seq에 index를 저장할 배열 초기화
        seq_index = []
        words = tokenizing_data(seq)
        for word in words:
            if dictionary.get(word):
                # seq_index에 dictionary 안의 인덱스를 extend 한다
                seq_index.extend([dictionary.get(word)])
            else:
                # dictionary에 존재 하지 않는 다면 UNK 값을 extend 한다 
                # seq_index.extend([UNK])
                seq_index.extend([UNK_INDEX])
        # 문장 제한 길이보다 길어질 경우 뒤에 토큰을 제거
        if len(seq_index) > DEFINES.max_sequence_length:
            seq_index = seq_index[:DEFINES.max_sequence_length]
        # seq의 길이를 저장
        seq_len.append(len(seq_index))
        # DEFINES.max_sequence_length 길이보다 작은 경우 PAD 값을 추가 (padding)
        # seq_index += [PAD] * (DEFINES.max_sequence_length - len(seq_index))
        seq_index += [PAD_INDEX] * (DEFINES.max_sequence_length - len(seq_index))

        # 인덱스화 되어 있는 값은 seq_input_index에 추가
        seq_input_index.append(seq_index)
    # print(np.array(seq_input_index))
    return np.array(seq_input_index)

# Req 1-2-2. 디코더에 필요한 데이터 전 처리 
def dec_input_processing(value, dictionary):

    # 인덱스 정보를 저장할 배열 초기화
    seq_input_index = []
    # 문장의 길이를 저장할 배열 초기화
    seq_len = []
    # 노이즈 캔슬
    value = prepro_noise_canceling(value)

    for seq in value:
        # 하나의 seq에 index를 저장할 배열 초기화
        seq_index = []
        # 디코딩 입력의 처음에는 START가 와야 하므로 STD 값 추가
        # seq_index.extend([STD])
        seq_index.extend([STD_INDEX])

        for word in seq.split():
            if dictionary.get(word) is not None:
                # seq_index에 dictionary 안의 인덱스를 extend 한다
                seq_index.extend([dictionary.get(word)])
            else:
                # dictionary에 존재 하지 않는 다면 UNK 값을 extend 한다
                # seq_index.extend([UNK])
                seq_index.extend([UNK_INDEX])
        # 문장 제한 길이보다 길어질 경우 뒤에 토큰을 제거
        if len(seq_index) > DEFINES.max_sequence_length:
            seq_index = seq_index[:DEFINES.max_sequence_length]
            
        # seq의 길이를 저장
        seq_len.append(seq_index)
        
        # DEFINES.max_sequence_length 길이보다 작은 경우 PAD 값을 추가 (padding)
        # seq_index += [PAD] * (DEFINES.max_sequence_length - len(seq_index))
        seq_index += [PAD_INDEX] * (DEFINES.max_sequence_length - len(seq_index))

        # 인덱스화 되어 있는 값은 seq_input_index에 추가
        seq_input_index.append(seq_index)
    # print(np.array(seq_input_index))
    return np.array(seq_input_index)

# Req 1-2-3. 디코더에 필요한 데이터 전 처리 
def dec_target_processing(value, dictionary):
    
    # 인덱스 정보를 저장할 배열 초기화
    seq_input_index = []
    # 문장의 길이를 저장할 배열 초기화
    seq_len = []
    # 노이즈 캔슬
    value = prepro_noise_canceling(value)
    
    for seq in value:
        
        # 하나의 seq에 index를 저장할 배열 초기화
        seq_index =[]
        
        for word in seq.split():
            if dictionary.get(word) is not None:
                # seq_index에 dictionary 안의 인덱스를 extend 한다
                seq_index.extend([dictionary.get(word)])
            else:
                # dictionary에 존재 하지 않는 다면 UNK 값을 extend 한다
                # seq_index.extend([UNK])
                seq_index.extend([UNK_INDEX])
        # 문장 제한 길이보다 길어질 경우 뒤에 토큰을 제거
        if len(seq_index) > DEFINES.max_sequence_length:
            seq_index = seq_index[:DEFINES.max_sequence_length-1]
        # END 토큰을 추가 (DEFINES.max_sequence_length 길이를 맞춰서 추가)
        # seq_index.extend([END])
        seq_index.extend([END_INDEX])

        # seq의 길이를 저장
        seq_len.append(len(seq_index))
        
        # DEFINES.max_sequence_length 길이보다 작은 경우 PAD 값을 추가 (padding)
        # seq_index += [PAD] * (DEFINES.max_sequence_length - len(seq_index))
        seq_index += [PAD_INDEX] * (DEFINES.max_sequence_length - len(seq_index))

        # 인덱스화 되어 있는 값은 seq_input_index에 추가
        seq_input_index.append(seq_index)
    # print(np.array(seq_input_index))
    return np.array(seq_input_index)

# input과 output dictionary를 만드는 함수
def in_out_dict(input, output, target):
    features = {"input": input, "output": output}
    return features, target


# 학습에 들어가 배치 데이터를 만드는 함수
def train_input_fn(train_input_enc, train_input_dec, train_target_dec, batch_size):
    # Dataset을 생성하는 부분으로써 from_tensor_slices부분은
    # 각각 한 문장으로 자른다고 보면 된다.
    # train_input_enc, train_output_dec, train_target_dec
    # 3개를 각각 한문장으로 나눈다.
    dataset = tf.data.Dataset.from_tensor_slices((train_input_enc, train_input_dec, train_target_dec))
    # 전체 데이터를 썩는다.
    dataset = dataset.shuffle(buffer_size=len(train_input_enc))
    # 배치 인자 값이 없다면  에러를 발생 시킨다.
    assert batch_size is not None, "train batchSize must not be None"
    # from_tensor_slices를 통해 나눈것을
    # 배치크기 만큼 묶어 준다.
    dataset = dataset.batch(batch_size, drop_remainder=True)
    # 데이터 각 요소에 대해서 in_out_dict 함수를
    # 통해서 요소를 변환하여 맵으로 구성한다.
    dataset = dataset.map(in_out_dict)
    # repeat()함수에 원하는 에포크 수를 넣을수 있으면
    # 아무 인자도 없다면 무한으로 이터레이터 된다.
    dataset = dataset.repeat()
    # make_one_shot_iterator를 통해 이터레이터를
    # 만들어 준다.
    iterator = dataset.make_one_shot_iterator()
    # 이터레이터를 통해 다음 항목의 텐서
    # 개체를 넘겨준다.
    return iterator.get_next()


# 평가에 들어가 배치 데이터를 만드는 함수
def eval_input_fn(eval_input_enc, eval_input_dec, eval_target_dec, batch_size):
    # Dataset을 생성하는 부분으로써 from_tensor_slices부분은
    # 각각 한 문장으로 자른다고 보면 된다.
    # eval_input_enc, eval_input_dec, eval_target_dec
    # 3개를 각각 한문장으로 나눈다.
    dataset = tf.data.Dataset.from_tensor_slices((eval_input_enc, eval_input_dec, eval_target_dec))
    # 전체 데이터를 섞는다.
    dataset = dataset.shuffle(buffer_size=len(eval_input_enc))
    # 배치 인자 값이 없다면  에러를 발생 시킨다.
    assert batch_size is not None, "eval batchSize must not be None"
    # from_tensor_slices를 통해 나눈것을
    # 배치크기 만큼 묶어 준다.
    dataset = dataset.batch(batch_size, drop_remainder=True)
    # 데이터 각 요소에 대해서 in_out_dict 함수를
    # 통해서 요소를 변환하여 맵으로 구성한다.
    dataset = dataset.map(in_out_dict)
    # repeat()함수에 원하는 에포크 수를 넣을수 있으면
    # 아무 인자도 없다면 무한으로 이터레이터 된다.
    # 평가이므로 1회만 동작 시킨다.
    dataset = dataset.repeat(1)
    # make_one_shot_iterator를 통해
    # 이터레이터를 만들어 준다.
    iterator = dataset.make_one_shot_iterator()
    # 이터레이터를 통해 다음 항목의
    # 텐서 개체를 넘겨준다.
    return iterator.get_next()
    
# Req 1-3-1. 단어 사전 파일 vocabularyData.voc를 생성하고 단어와 인덱스 관계를 출력
def load_voc():
    # 사전을 담을 배열 준비한다.
    voc_list = []
    # 사전을 구성한 후 파일로 저장 진행한다.
    # 그 파일의 존재 유무를 확인한다.
    if (not (os.path.exists(DEFINES.vocabulary_path))):
        # 이미 생성된 사전 파일이 존재하지 않으므로
        # 데이터를 가지고 만들어야 한다.
        # 그래서 데이터가 존재 하면 사전을 만들기 위해서
        # 데이터 파일의 존재 유무를 확인한다.

        data_df = pd.read_csv(DEFINES.data_path)
        # 판다스의 데이터 프레임을 통해
        # 질문과 답에 대한 열을 가져 온다.
        question, answer = data_df['Q'], data_df['A']
        data_set = []
        # 질문과 답변을 extend을
        # 통해서 구조가 없는 배열로 만든다.
        data_set.extend(question)
        data_set.extend(answer)

        # data를 토크나이즈하여 words에 저장한다.
        words = []
        for data in data_set:
            words.extend(tokenizing_data(data))
        # 중복되는 단어(토큰)를 제거
        print(words)
        words = list(set(words))

        # 데이터 없는 내용중에 MARKER 추가
        words[:0] = MARKER

        # 사전 파일을 생성
        # DEFINES.vocabulary_path에 words안에 저장된 가 단어(토큰)들을 한줄 씩 저장
        with open(DEFINES.vocabulary_path, 'w', encoding='utf-8') as voc_file:
            for word in words:
                voc_file.write(word+"\n")

    # 사전 파일에서 단어(토큰)을 가져와 voc_list에 저장
    with open(DEFINES.vocabulary_path, 'r', encoding='utf-8') as voc_file:
        for line in voc_file:
            voc_list.append(line[:-1])

    # make() 함수를 사용하여 dictionary 형태의 char2idx, idx2char 저장
    char2idx, idx2char = make_voc(voc_list)

    return char2idx, idx2char, len(voc_list)

# Req 1-3-2. 사전 리스트를 받아 인덱스와 토큰의 dictionary를 생성
def make_voc(voc_list):
    char2idx = {char: idx for idx, char in enumerate(voc_list)}
    idx2char = {idx: char for idx, char in enumerate(voc_list)}

    return char2idx, idx2char

# Req 1-3-3. 예측용 단어 인덱스를 문장으로 변환
def pred_next_string(value, dictionary):
    result = []
    for v in value:
        print(v)
        print(v['indexs'])
        for i in v['indexs']:
            if dictionary.get(i):
                result.append(dictionary.get(i))
    print(result)
    answer = ""
    for word in result:
        if word not in PAD and word not in END:
            answer += word
            answer += " "

    print(answer)
    return answer, True
    

def main(self):
    char2idx, idx2char, voc_length = load_voc()
    # train_q, train_a, test_q, test_a = load_data()
    # enc_processing(train_q, char2idx)
    # print(pred_next_string([4, 62, 473, 4423, 2354, 2, 46], idx2char))

if __name__ == '__main__':
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run(main)



# prepro_train_q = prepro_noise_canceling(train_q)
# dictionary = tokenizing_data(prepro_train_q)
# enc_train_q = enc_processing(train_q, dictionary)
# dec_train_a = dec_input_processing(train_a, dictionary)
# dec_target_processing(train_a, dictionary)
