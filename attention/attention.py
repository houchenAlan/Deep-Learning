from keras.layers import Bidirectional, Concatenate, Dot, Input, LSTM
from keras.layers import RepeatVector, Dense, Activation, Lambda
from keras.optimizers import Adam
from keras.models import  Model
import keras.backend as K
import numpy as np
import random as random
import json


def tokenize(sentence, vocab, length):
    tokens = [0] * length
    for i in range(length):
        char = sentence[i] if i < len(sentence) else "<pad>"
        char = char if (char in vocab) else "<unk>"
        tokens[i] = vocab[char]
    return tokens
def readyData(dataset, human_vocab, machine_vocab, Tx, Ty):
    m = len(dataset)
    X = np.zeros([m, Tx], dtype='int32')
    Y = np.zeros([m, Ty], dtype='int32')
    for i in range(m):
        data = dataset[i]
        X[i] = np.array(tokenize(data[0], human_vocab, Tx))
        Y[i] = np.array(tokenize(data[1], machine_vocab, Ty))
    Xoh = oh_2d(X, len(human_vocab))
    Yoh = oh_2d(Y, len(machine_vocab))
    return (X, Y, Xoh, Yoh)


def ids2keys(sentence, vocab):
    return [list(vocab.keys())[id] for id in sentence]

def oh_2d(dense, max_value):

    oh = np.zeros(np.append(dense.shape, [max_value]))
    ids1, ids2 = np.meshgrid(np.arange(dense.shape[0]), np.arange(dense.shape[1]))
    oh[ids1.flatten(), ids2.flatten(), dense.flatten('F').astype(int)] = 1
    return oh

def get_prediction(model, x):
    prediction = model.predict(x)
    max_prediction = [y.argmax() for y in prediction]
    str_prediction = "".join(ids2keys(max_prediction, machine_vocab))
    return (max_prediction, str_prediction)
def get_model(Tx, Ty, layer1_size, layer2_size, x_vocab_size, y_vocab_size):
    X = Input(shape=(Tx, x_vocab_size))
    a1 = Bidirectional(LSTM(layer1_size, return_sequences=True), merge_mode='concat')(X)
    a2 = attention_layer(a1, layer2_size, Ty)
    a3 = [layer3(timestep) for timestep in a2]
    model = Model(inputs=[X], outputs=a3)
    return model
def one_step_of_attention(h_prev, a):
    h_repeat = at_repeat(h_prev)
    i = at_concatenate([a, h_repeat])
    i = at_dense1(i)
    i = at_dense2(i)
    attention = at_softmax(i)
    context = at_dot([attention, a])
    return context
def softmax(x):
    return K.softmax(x, axis=1)
def attention_layer(X, n_h, Ty):
    h = Lambda(lambda X: K.zeros(shape=(K.shape(X)[0], n_h)))(X)
    c = Lambda(lambda X: K.zeros(shape=(K.shape(X)[0], n_h)))(X)
    at_LSTM = LSTM(n_h, return_state=True)
    output = []
    for _ in range(Ty):
        context = one_step_of_attention(h, X)
        h, _, c = at_LSTM(context, initial_state=[h, c])
        output.append(h)
    return output
with open('data/Time Dataset.json', 'r') as f:
    dataset = json.loads(f.read())
with open('data/Time Vocabs.json', 'r') as f:
    human_vocab, machine_vocab = json.loads(f.read())
human_vocab_size = len(human_vocab)
machine_vocab_size = len(machine_vocab)
m = len(dataset)
Tx = 41
Ty = 5
X, Y, Xoh, Yoh = readyData(dataset, human_vocab, machine_vocab, Tx, Ty)
train_size = int(0.8*m)
Xoh_train = Xoh[:train_size]
Yoh_train = Yoh[:train_size]
Xoh_test = Xoh[train_size:]
Yoh_test = Yoh[train_size:]
layer1_size = 32
layer2_size = 64
at_repeat = RepeatVector(Tx)
at_concatenate = Concatenate(axis=-1)
at_dense1 = Dense(8, activation="tanh")
at_dense2 = Dense(1, activation="relu")
at_softmax = Activation(softmax, name='attention_weights')
at_dot = Dot(axes=1)
layer3 = Dense(machine_vocab_size, activation=softmax)
model = get_model(Tx, Ty, layer1_size, layer2_size, human_vocab_size, machine_vocab_size)
opt = Adam(lr=0.05, decay=0.04, clipnorm=1.0)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
outputs_train = list(Yoh_train.swapaxes(0,1))
model.fit([Xoh_train], outputs_train, epochs=30, batch_size=100)
outputs_test = list(Yoh_test.swapaxes(0,1))
score = model.evaluate(Xoh_test, outputs_test)
print('Test loss: ', score[0])
i = random.randint(0, m)
max_prediction, str_prediction = get_prediction(model, Xoh[i:i+1])
print("Input: " + str(dataset[i][0]))
print("Tokenized: " + str(X[i]))
print("Prediction: " + str(max_prediction))
print("Prediction text: " + str(str_prediction))
