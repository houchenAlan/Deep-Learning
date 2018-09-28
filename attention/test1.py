from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.layers import Dense,Embedding,SimpleRNN
from keras import Sequential
import matplotlib.pyplot as plt
max_feature=10000
max_len=500
batch_size=32
print('Loading data...')
(input_train,y_train),(input_test,y_test)=imdb.load_data(num_words=max_feature)
print(len(input_train),"train sequence")
print(len(input_test),"test sequence")
print("Pad sequences (samples x time)")
input_train=sequence.pad_sequences(input_train,maxlen=max_len)
input_test=sequence.pad_sequences(input_test,maxlen=max_len)
print("input_train shape:",input_train.shape)
print("input_test shape:",input_test.shape)
model=Sequential()
model.add(Embedding(max_feature,32))
model.add(SimpleRNN(32))
model.add(Dense(1,activation="sigmoid"))
model.compile(optimizer="rmsprop",loss="binary_crossentropy",metrics=['accuracy'])
history=model.fit(input_train,y_train,epochs=10,batch_size=128,validation_split=0.2)
acc=history.history["acc"]
val_acc=history.history["val_acc"]
loss=history.history["loss"]
val_loss=history.history["val_loss"]
epochs=range(1,len(acc)+1)
plt.plot(epochs,acc,'bo',label="Training acc")
plt.plot(epochs,val_acc,"b",label="Validation acc")
plt.title("Training and validation accuracy")
plt.legend()
plt.show()