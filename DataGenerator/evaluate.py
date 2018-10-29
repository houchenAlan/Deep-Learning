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
    if str(dfUser.loc[userId]["gender"])=="女" and int(dfUser.loc[userId]["age"])>=16:
        curlist=dfItem[dfItem["secondClass"]=="女士保暖" ].index.tolist()
        sumList.extend(curlist)
    if str(dfUser.loc[userId]["gender"]) == "男" and int(dfUser.loc[userId]["age"])>=16:
        curlist = dfItem[dfItem["secondClass"] == "男士保暖"].index.tolist()
        sumList.extend(curlist)
    if str(dfUser.loc[userId]["gender"]) == "男" and int(dfUser.loc[userId]["age"])>=25:
        curlist=dfItem[dfItem["secondClass"]=="瑞士名表"].index.tolist()
        sumList.extend(curlist)
    if str(dfUser.loc[userId]["haveBaby"])=="是" and int(dfUser.loc[userId]["age"])<=35:
        curlist = dfItem[dfItem["firstClass"] == "母婴童装"].index.tolist()
        sumList.extend(curlist)
    if str(dfUser.loc[userId]["haveCar"])=="是":
        curlist = dfItem[dfItem["firstClass"] == "汽车用品"].index.tolist()
        sumList.extend(curlist)
    if str(dfUser.loc[userId]["career"])=="教师":
        curlist = dfItem[dfItem["secondClass"] == "教材教辅"].index.tolist()
        sumList.extend(curlist)
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
print("accuracy:",'%0.2f'%np.mean(list1))