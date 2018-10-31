#coding:UTF-8
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
dfUser=pd.read_csv("/Users/admin/PycharmProjects/Deep-Learning/DataGenerator/data/user.csv")
dfItem=pd.read_csv("/Users/admin/PycharmProjects/Deep-Learning/DataGenerator/data/item.csv")
dfEvent=pd.read_csv("/Users/admin/PycharmProjects/Deep-Learning/DataGenerator/data/event.csv")
dfUE=pd.merge(dfEvent,dfUser)
data=pd.merge(dfUE,dfItem)
X=data[["gender","age","edu","marriageState","career","haveBaby","salary","homeTown","residence","haveCar","haveHouse","firstClass","secondClass","price","size","seasonable"]]
y=data["label"]
#X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
#print(X_train.shape)
#print(X_test.shape)
#print(X_train.head())
enc=OneHotEncoder(categorical_features=[0,2,3,4,5,7,8,9,10,11,12,14,15],handle_unknown=True)
X=enc.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

print(X_train.shape)
print(y_train.shape)
lr=LogisticRegression(solver='liblinear')

lr.fit(X_train,y_train)

print(lr.predict_proba(X)[:,1])

print("trainSet accuracy:%0.3f"%lr.score(X_train,y_train))
print("testSet accuracy:%0.3f"%lr.score(X_test,y_test))
print("coef_:",lr.coef_.reshape(-1,1))
print(lr.get_params())




