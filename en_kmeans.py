
from sklearn.feature_extraction.text import TfidfVectorizer  # 基于TF-IDF的词频转向量库
from sklearn.cluster import KMeans
import jieba.posseg as pseg

import datetime as dt
today = dt.datetime.today().strftime("%Y-%m-%d")  # 过去今天时间

x=rand(1,1)

ypred=(y-ypre)**2

stopwords=[]
with open('data/stopwords.txt',encoding='utf_')as f:
    for line in f:
        stopwords.append(line.strip())


from keyword_extraction import get_text

f=open('data/data.txt',encoding='utf_')
texts=[]
for line in f.readlines():
    texts.append(line.strip().split('\t')[0])

"""
预处理文本
"""

comment_texts,_=get_text(texts)

vectorizer = TfidfVectorizer(stop_words=stopwords,   use_idf=True)  # 创建词向量模型
X = vectorizer.fit_transform(comment_texts)

model_kmeans = KMeans(n_clusters=5)  # 创建聚类模型对象
model_kmeans.fit(X)  # 训练模型
