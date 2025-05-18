import pandas as pd
from sklearn.model_selection import train_test_split
data = pd.read_csv("heart.csv")
train,test = train_test_split(data, test_size=0.1, random_state=42)
train.to_csv('train.csv',index=False)
test.to_csv('test.csv',index=False)