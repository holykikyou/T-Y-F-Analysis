# pip install pytextrank
# python -m spacy download en_core_web_sm
import spacy
#-*-coding:utf-8-*-
import codecs
import json
import os
import string
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet
import re

import sys
"""
去停用词
"""
p1 = re.compile(r'-\{.*?(zh-hans|zh-cn):([^;]*?)(;.*?)?\}-')
p2 = re.compile(r'[(][: @ . , ？！\s][)]')
p3 = re.compile(r'[「『]')
p4 = re.compile(r'[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）0-9 , : ; \-\ \[\ \]\ ]')


"""
基于lda主题模型
"""
from gensim import corpora, models
import jieba.posseg as jp
import jieba

stopwords=[]
with open('data/stopwords.txt',encoding='utf_')as f:
    for line in f:
        stopwords.append(line.strip())




words_list=[]
# 简单文本处理
def get_text(texts):
    """
    输出句子列表和单词列表
    """
    wnl = WordNetLemmatizer()
    docs = [doc.lower() for doc in texts]
    for c in string.punctuation:  # 去标点
        docs = [doc.replace(c, ' ')for doc in docs]
    for c in string.digits:  # 去数字
        docs = [doc.replace(c, '')for doc in docs]
    docs = [nltk.word_tokenize(doc) for doc in docs]
    # nlp=spacy.load('en_core_web_sm')
    words_list=[]
    sentence_list=[]
    # sentence_list=[ nlp(sentence)for sentence in texts]

    for doc in docs:
        word_list=[]
        sentence=''
        for word in doc:
            if len(word) >= 3 and word not in stopwords:
                word = wnl.lemmatize(word)  # 词形还原
                word_list.append(word)
                sentence=sentence+word+' '
        words_list.append(word_list)
        sentence_list.append(sentence.strip())
    return sentence_list,words_list



# 生成LDA模型
def LDA_model(words_list):
    # 构造词典
    # Dictionary()方法遍历所有的文本，为每个不重复的单词分配一个单独的整数ID，同时收集该单词出现次数以及相关的统计信息
    dictionary = corpora.Dictionary(words_list)
    print(dictionary)
    print('打印查看每个单词的id:')
    print(dictionary.token2id)  # 打印查看每个单词的id

    # 将dictionary转化为一个词袋
    # doc2bow()方法将dictionary转化为一个词袋。得到的结果corpus是一个向量的列表，向量的个数就是文档数。
    # 在每个文档向量中都包含一系列元组,元组的形式是（单词 ID，词频）
    corpus = [dictionary.doc2bow(words) for words in words_list]

    print('输出每个文档的向量:')
    print(corpus)  # 输出每个文档的向量

    # LDA主题模型
    # num_topics -- 必须，要生成的主题个数。
    # id2word    -- 必须，LdaModel类要求我们之前的dictionary把id都映射成为字符串。
    # passes     -- 可选，模型遍历语料库的次数。遍历的次数越多，模型越精确。但是对于非常大的语料库，遍历太多次会花费很长的时间。
    lda_model = models.ldamodel.LdaModel(corpus=corpus, num_topics=2, id2word=dictionary, passes=10)

    return lda_model


if __name__ == "__main__":
    f=open('data/data.txt',encoding='utf_')
    texts=[]
    for line in f.readlines():
        texts.append(line.strip().split('\t')[0])
    print(texts)
    _,words_list = get_text(texts)
    print('分词后的文本：')
    print(words_list)

    # 获取训练后的LDA模型
    lda_model = LDA_model(words_list)

    # 可以用 print_topic 和 print_topics 方法来查看主题
    # 打印所有主题，每个主题显示5个词
    topic_words = lda_model.print_topics(num_topics=2, num_words=5)
    print('打印所有主题，每个主题显示5个词:')
    print(topic_words)

    # 输出该主题的的词及其词的权重
    words_list = lda_model.show_topic(0, 5)
    print('输出该主题的的词及其词的权重:')
    print(words_list)
    f.close()