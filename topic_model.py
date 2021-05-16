"""
data:2021/05/07
author:liuyiding
topicmodel:lsi,lda
textsummary:textrank,lsa,

判断文本需求，要对具体任务做具体的调整，比如停用词典里加入戴琦id，美国之类的常见无意义词汇，防止错误召回
如
ambassador
katherine
tai
washington
–"
Sarah
Bianchi
"""

from utils import expand_contrations,word_tokenize


from gensim import  corpora,models

import re

import sys

def remove_stopwords(tokens,stopwords_file):
    """
    原文分词后单词列表（一维）
    去掉其中的停止词
    去除特殊字符
    """
    import nltk
    #nltk.download('stopwords')#已经下载过一次
    stopwords_lists=[]
    with open(stopwords_file,encoding='utf_8',mode='r')as f:
        for word in f.readlines():
            stopwords_lists.append(word.strip())

    filter_words = [token for token in tokens if token not in stopwords_lists]
    return filter_words


def normalize_corpus(corpus, lemmatize=False):
    # 输入文档列表，返回二维的列表，其中每个元素都是一个文档的词列表
    normalize_corpus = []
    text_list = [remove_special_characters(text) for text in corpus]  # 去掉特殊符号的原始的英文文本列表，较好的输入
    for text in text_list:
        text = expand_contrations(text)
        if (lemmatize):
            pass
        else:
            text = text.lower()
        text = word_tokenize(text)
        normalize_corpus.append(text)
        #print(text)
    normalize_corpus = [remove_stopwords(text,'stopwords.txt')for text in normalize_corpus]
    return normalize_corpus
def remove_special_characters(text):
    """
    和另一个文件的同名函数不一样
    :param all_text:文档
    :return: 清洗特殊符号后的句子列表
    """

    import string

    pattern=re.compile('[{}]'.format(re.escape(string.punctuation)))#去除特殊字符和符号的正则表达式
    sentence_list=pattern.sub('',text)
    return sentence_list


def get_corpus(input_file):
    # 获取全部文本
    all_text = []
    entext_pattern = re.compile('[a-zA-Z]')
    with open(input_file, encoding='utf_8', mode='r')as f:
        for line in f:
            if (entext_pattern.findall(line)):
                all_text.append(line.strip())  # 筛选有英文文本内容的行
    return all_text


def train_lda_model_gensim(normed_corpus, total_topics=4,feature_mode='tf_idf'):
    dictionary = corpora.Dictionary(normed_corpus)
    mapped_corpus = [dictionary.doc2bow(text) for text in normed_corpus]
    if feature_mode=='tf_idf':
        tfidf = models.tfidfmodel.TfidfModel(mapped_corpus)
        corpus_tfidf = tfidf[mapped_corpus]
        lda = models.ldamodel.LdaModel(corpus_tfidf, iterations=50, id2word=dictionary, passes=10,
                                       num_topics=total_topics)
    else:
        lda = models.ldamodel.LdaModel(mapped_corpus,iterations=100, id2word=dictionary, passes=10, num_topics=total_topics)
    return lda


def print_ans(normed_corpus,num_topics=4,method='lda'):
    if method == 'lda':
        lda_model = train_lda_model_gensim(normed_corpus)
        topic_words = lda_model.print_topics(num_topics, num_words=8)
        print('打印所有主题，每个主题显示8个词:')
        print(topic_words)


import os
#每行一个段落，或者每行一句话的格式应该都可以


# input_file=sys.argv[1]#文本文件
# input_file = 'test.txt'



# corpus=get_corpus(input_file)
def load_data():
    corpus=get_corpus('tweet_data/戴琦推文.txt')
    try:
        corpus.extend(get_corpus('tweet_data/官网推文.txt'))
    except:
        pass
    return corpus



corpus=load_data()
normed_corpus=normalize_corpus(corpus)#去停用词等操作
for i in range(10):
    print_ans(normed_corpus)


