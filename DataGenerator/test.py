import  pandas as pd
df=pd.DataFrame(columns=["userId","itemId","eventType","score"])
df.loc[0]=[1,1,2,80]
df.loc[1]=[2,1,4,70]
df.loc[2]=[1,2,3,90]
df.loc[3]=[2,2,3,100]
#df.groupby(by=['userId']).to_frame()
print(df)
print(df.loc[1]["score"])
print(len(df))