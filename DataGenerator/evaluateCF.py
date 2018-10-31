# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
import random

dfResult=pd.read_csv("/Users/admin/PycharmProjects/Deep-Learning/DataGenerator/data/part-00000")
dfResult.columns=["userId","itemId","score"]
dfUser=pd.read_csv("/Users/admin/PycharmProjects/Deep-Learning/DataGenerator/data/user.csv")
print(dfUser)
dfItem=pd.read_csv("/Users/admin/PycharmProjects/Deep-Learning/DataGenerator/data/item.csv")
#总规则
def getItemIdwithUserId(userId,itemId):
    sumList=[]
    #规则明细
    if dfUser.loc[userId]["gender"]==0 and int(dfUser.loc[userId]["age"])>=16:#大雨16岁的女
        curlist=dfItem[dfItem["secondClass"]==33 ].index.tolist() #女士保暖
        sumList.extend(curlist)
        print("规则1")
    if dfUser.loc[userId]["gender"] == 1 and int(dfUser.loc[userId]["age"])>=16: #大于16岁的男
        curlist = dfItem[dfItem["secondClass"] == 32].index.tolist() #
        sumList.extend(curlist)
        print("规则2")
    if dfUser.loc[userId]["gender"] == 1 and int(dfUser.loc[userId]["age"])>=25: #大于25岁的男
        curlist=dfItem[dfItem["secondClass"]==0].index.tolist()  #瑞士名表
        sumList.extend(curlist)
        print("规则3")
    if dfUser.loc[userId]["haveBaby"]==1 and int(dfUser.loc[userId]["age"])<=35: #有小孩且小于35岁
        curlist = dfItem[dfItem["firstClass"] == 9].index.tolist() #母婴童装
        sumList.extend(curlist)
        print("规则4")
    if dfUser.loc[userId]["haveCar"]==1: #有车
        curlist = dfItem[dfItem["firstClass"] == 12].index.tolist()  #汽车用品
        sumList.extend(curlist)
        print("规则5")
    if dfUser.loc[userId]["career"]==2:  #教师
        curlist = dfItem[dfItem["secondClass"] == 102].index.tolist()  #教材教辅
        sumList.extend(curlist)
        print("规则6")
    print(len(sumList))
    if itemId not in sumList:
        return 0
    else:
        return 1
list1=[]
for i in range(len(dfResult)):
    curuserId=int(dfResult.loc[i]["userId"])
    curitemId=int(dfResult.loc[i]["itemId"])
    result=getItemIdwithUserId(curuserId,curitemId)
    list1.append(result)
    print(curuserId,curitemId,result)
print("accuracy:%0.3f"%np.mean(list1))