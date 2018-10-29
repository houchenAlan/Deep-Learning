#encoding:UTF-8
import pandas as pd
import random
import numpy as np
userCount=1000
itemCount=1000
eventCount=10000
#---------------------------userInfo-------------------------------
#用户ID，性别，年龄，教育程度，婚否，职业，有无孩子，薪资，家乡，常住地，有无车，有无房
userColumns=["userId","gender","age","edu","marriageState","career","haveBaby","salary","homeTown","residence","haveCar","haveHouse"]
#学历
eduMap={0:"未知",1:"小学",2:"初中",3:"高中",4:"大专",5:"本科",6:"硕士",7:"博士"}
#婚姻状态
marriageMap={0:"未婚",1:"已婚",2:"离异"}
#职业
careerMap={0:"未知",1:"学生",2:"教师",3:"医生",4:"程序员",5:"销售",6:"建筑师"}
#家乡和常住地
homeAndResidence={0:"北京",1:"上海",2:"广州",3:"深圳",4:"西安",5:"武汉",6:"长沙",7:"贵阳",8:"厦门",9:"杭州",10:"济南",11:"烟台",12:"南京"}

#-----约束-----
def geneGender():#生成性别
    randGender = random.uniform(0, 10)  # 生成均匀分布随机数
    if randGender<5:
        return "女"
    else:
        return "男"
def geneAge():#生成年龄
    randAge=random.gauss(40,25)
    if randAge>0 and randAge<100:
        return round(randAge)
    else:
        return 0
def geneEduWithAge(age):#生成学历
    if age<3:
        return "未知"
    elif age<=13:
        return eduMap[random.randint(0,1)]
    elif age<=15:
        return eduMap[random.randint(0,2)]
    elif age<=18:
        return eduMap[random.randint(0,3)]
    elif age<=22:
        return eduMap[random.randint(0,5)]
    elif age<=25:
        return eduMap[random.randint(0,6)]
    else:
        return eduMap[random.randint(0,7)]
def geneMarriageWithAgeAndGender(geneder,age):#生成婚否
    if gender=="男" and age<22:
        return "未婚"
    if gender=="女" and age<20:
        return "未婚"
    return marriageMap[random.randint(0,2)]
def geneHaveBaby(marriageState):
    if marriageState=="未婚":
        return "否"
    return random.choice(["是","否"])
def geneSalary():
    salaryNum=random.gauss(10000,6000)
    if salaryNum<0:
        return 0
    return round(salaryNum)
def geneHomeAndResidence():
    return homeAndResidence[random.randint(0,len(homeAndResidence)-1)]

dfUser=pd.DataFrame(columns=userColumns)
print("正在生成User信息。。。")
for i in range(userCount):
    userId=i
    gender=geneGender()
    age=geneAge()
    edu=geneEduWithAge(age)
    marriageState=geneMarriageWithAgeAndGender(gender,age)
    carrer=careerMap[random.randint(0,len(careerMap)-1)]
    haveBaby=geneHaveBaby(marriageState)
    salary=geneSalary()
    homeTown=geneHomeAndResidence()
    residence=geneHomeAndResidence()
    haveCar=random.choice(["是","否"])
    haveHouse=random.choice(["是","否"])
    dfUser.loc[i]=[userId,gender,age,edu,marriageState,carrer,haveBaby,salary,homeTown,residence,haveCar,haveHouse]
dfUser.to_csv("./data/user.csv",index=False)
print("User信息以生成！！！")
#---------------------------itemInfo-------------------------------
#物品ID，商品名称，一级类目，二级类目，价格，型号，季节性，
itemColumns=["itemId","itemName","firstClass","secondClass","price","size","seasonable"]
#分类map
classMap={"奢侈品":{"瑞士名表":[],"手镯":[],"项链":[],"耳饰":[]},
"男装":{"夹克":[],"休闲裤":[],"T恤":[],"牛仔裤":[],"衬衫":[],"风衣":[],"风衣":[],"西服":[]},
"女装":{"套装裙":[],"羊绒大衣":[],"毛衣外套":[],"学生卫衣":[],"加绒打底裤":[],"小脚裤":[],"妈妈装":[],"旗袍":[]},
"内衣配饰":{"保暖上衣":[],"保暖裤":[],"男士保暖":[],"女士保暖":[],"睡衣":[],"男士睡衣":[],"女士睡衣":[],"文胸":[],"内裤":[],"平角内裤":[],"低腰内裤":[]},
"箱包手袋":{"时尚男包":[],"男士腰带":[],"拉杆箱":[],"电脑包":[],"学生书包":[],"自营女包":[],"化妆包":[],"卡包":[]},
"美妆护肤":{"护肤礼盒":[],"卸妆":[],"洁面":[],"敏感肌":[],"眼霜":[],"面膜":[],"唇膏":[],"抗痘":[],"香水":[],"CC霜":[]},
"手机数码":{"游戏手机":[],"拍照手机":[],"全面屏手机":[],"女性手机":[],"长续航手机":[],"老人机":[],"单反相机":[],"摄像机":[],"音箱":[],"电子词典":[]},
"电脑办公":{"吃鸡装备":[],"游戏本":[],"轻薄本":[],"游戏台式机":[],"机械键盘":[],"曲屏显示器":[],"组装电脑":[],"显卡":[],"家用打印机":[],"投影仪":[]},
"家用电器":{"电视":[],"空调":[],"洗衣机":[],"冰箱":[],"厨卫大电":[],"厨房小电":[],"生活电器":[],"个护健康":[],"家庭影音":[]},
"母婴童装":{"奶粉":[],"营养辅食":[],"尿裤湿巾":[],"喂养用品":[],"洗护用品":[],"童车童床":[],"妈妈专区":[],"安全座椅":[],"童装":[]},
"图书音箱":{"童书":[],"文学小说":[],"教材教辅":[],"人文社科":[],"经管励志":[],"IT科技":[],"文娱":[]},
"运动户外":{"跑步鞋":[],"足球鞋":[],"鱼竿鱼线":[],"跑步机":[],"山地车":[],"登山靴":[],"健身服":[],"户外工具":[]},
"汽车用品":{"汽车坐垫":[],"行车记录仪":[],"机油":[],"洗车水枪":[],"轮胎":[],"导航仪":[],"安全预警仪":[],"防冻油":[]}}

dfItem=pd.DataFrame(columns=itemColumns)
itemId=0
print("正在生成Item信息。。。")
for k1,v1 in classMap.items():
    firstClass=k1
    for k2,v2 in v1.items():
        secondClass=k2
        for i in range(10):
            itemName=k2+str(i)+"号"
            v2.append(itemName)
            price=round(random.gauss(1000,500))
            size=random.choice(["无","小","中","大"])
            seasonable=random.choice(["无","春","夏","秋","冬"])
            dfItem.loc[itemId]=[itemId,itemName,firstClass,secondClass,price,size,seasonable]
            itemId=itemId+1
dfItem.to_csv("./data/item.csv",index=False)
print("Item信息已生成！！！")
print("size:",itemId)
#---------------------------eventInfo-------------------------------
eventColumns=["userId","itemId","score","time"]
#总规则
def getItemIdwithUserId(userId):
    sumItemId=range(itemId)
    sumList=[]  #订购list
    ranNum=np.random.uniform()
    print(ranNum)
    #规则明细
    if str(dfUser.loc[userId]["gender"])=="女" and int(dfUser.loc[userId]["age"])>=16:
        curlist=dfItem[dfItem["secondClass"]=="女士保暖" ].index.tolist()
        sumList.extend(curlist)
        print("规则1")
    if str(dfUser.loc[userId]["gender"]) == "男" and int(dfUser.loc[userId]["age"])>=16:
        curlist = dfItem[dfItem["secondClass"] == "男士保暖"].index.tolist()
        sumList.extend(curlist)
        print("规则2")
    if str(dfUser.loc[userId]["gender"]) == "男" and int(dfUser.loc[userId]["age"])>=25:
        curlist=dfItem[dfItem["secondClass"]=="瑞士名表"].index.tolist()
        sumList.extend(curlist)
        print("规则3")
    if str(dfUser.loc[userId]["haveBaby"])=="是" and int(dfUser.loc[userId]["age"])<=35:
        curlist = dfItem[dfItem["firstClass"] == "母婴童装"].index.tolist()
        sumList.extend(curlist)
        print("规则4")
    if str(dfUser.loc[userId]["haveCar"])=="是":
        curlist = dfItem[dfItem["firstClass"] == "汽车用品"].index.tolist()
        sumList.extend(curlist)
        print("规则5")
    if str(dfUser.loc[userId]["career"])=="教师":
        curlist = dfItem[dfItem["secondClass"] == "教材教辅"].index.tolist()
        sumList.extend(curlist)
        print("规则6")

    #以80%的概率出现
    if ranNum<0.8 and len(sumList)>0:
        score=random.choice([4,5])
        print("if:",len(sumList))
        return score,sumList
    else:
        score=random.choice([1,2,3])
        set1=set(sumItemId)
        set2=set(sumList)
        set3=set1.difference(set2)
        sumList=list(set3)
        print("else:",len(sumList))
        return score,sumList

dfEvent=pd.DataFrame(columns=eventColumns)
eventCount=0
print("正在生成Event信息。。。")
for i in range(1000):
    curUserId=i
    eCount=50
    for j in range(eCount):
        curscore,curlist=getItemIdwithUserId(curUserId)
        curItemId=random.choice(curlist)
        score=curscore
        time=19930928
        dfEvent.loc[eventCount]=[curUserId,curItemId,score,time]
        eventCount=eventCount+1
dfEvent.to_csv("./data/event.csv",index=False,header=False)
print("Event信息已生成！！！")

