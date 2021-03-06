import pandas as pd
import json
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt

with open('train/scene_train_annotations_20170904.json', 'r') as f: #label文件
    label_raw = json.load(f)
    
with open('validation/scene_validation_annotations_20170908.json', 'r') as f: #label文件
    label_raw2 = json.load(f)
    

mlist = []
for _ in label_raw:
    mlist.append(_['label_id'])
    
mlist2 = []
for _ in label_raw2:
    mlist2.append(_['label_id'])
    
a = Counter(mlist)
print(min(a.values()))
print(max(a.values()))

b = Counter(mlist2)
print(min(b.values()))
print(max(b.values()))

mlist = [int(i) for i in mlist]
mlist2 = [int(i) for i in mlist2]
a1 = pd.DataFrame(mlist)
b1 = pd.DataFrame(mlist2)

plt.figure()
sns.countplot(x=0, data=a1)
plt.savefig("train_distribution.png")
plt.figure()
sns.countplot(x=0, data=b1)
plt.savefig("validation_distribution.png")

'''
类别可能存在一定的不平衡问题
'''


'''
训练集和验证集有没有重复先不管了
'''

class_sample_count = []
for i in range(0,80):
    class_sample_count.append(a[str(i)])