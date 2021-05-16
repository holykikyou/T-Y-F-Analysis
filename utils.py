"""
org:
author:刘一丁
time:2021.0424
"""


import sys
import re
import os




class My_Topic_model:
    def __init__(self,input_file):
        self.corpus=self.get_corpus(input_file)
        self.normed_corpus=normalize_corpus(self.corpus)#列表形式的文档集合



    def get_corpus(self,input_file):
        # 获取全部文本
        all_text = []
        entext_pattern = re.compile('[a-zA-Z]')
        with open(input_file, encoding='utf_8', mode='r')as f:
            for line in f:
                if (entext_pattern.findall(line)):
                    all_text.append(line.strip())#筛选有英文文本内容的行
        return all_text

    def train_lda_model_gensim(self,total_topics=4):
        dictionary=corpora.Dictionary(self.normed_corpus)
        mapped_corpus=[dictionary.doc2bow(text) for text in self.normed_corpus]
        # tfidf=models.tfidfmodel.TfidfModel(mapped_corpus)
        # corpus_tfidf=tfidf[mapped_corpus]
        #lda=models.ldamodel.LdaModel(corpus_tfidf,id2word=dictionary,passes=10,num_topics=total_topics)
        lda = models.ldamodel.LdaModel(mapped_corpus, id2word=dictionary, passes=10, num_topics=total_topics)
        return lda

    def print_ans(self,method='lda'):
        if method=='lda':
            lda_model=self.train_lda_model_gensim()
            topic_words = lda_model.print_topics(num_topics=2, num_words=5)
            print('打印所有主题，每个主题显示5个词:')
            print(topic_words)








"""
词频统计
"""
def find_token(text):
    """
    返回孤立单词，在做词频统计时没有考虑词组
    """

    return re.findall('[a-z]+',text.lower())


"""
使用nltk自带分句器和分词器
"""

def sentence_tokenize(all_text,keep_special=False):
    from nltk import sent_tokenize
    sentence_list=sent_tokenize(all_text)
    #pattern=re.compile(r'[^a-zA-Z0-9]')去除非英语数字文本
    pattern=re.compile(r'[?|,|.|(|)|<|-|>|%]')#去除撇号句号
    return [re.sub(pattern,r'',sentence) for sentence in sentence_list]




def nltk_tokenize(sentence_list):
    #不去除停止词
    from nltk import word_tokenize
    res=[word_tokenize(sentence) for sentence in sentence_list]
    #这里可以很简单返回一个一维的词表，但是可以用更有技巧的方式
    from functools import  reduce
    word_tokens=reduce(lambda x,y:x+y,res)#实现多个列表相加
    return word_tokens


def remove_stopwords(tokens):
    """
    原文分词后单词列表（一维）
    去掉其中的停止词
    去除特殊字符
    """
    import nltk
    #nltk.download('stopwords')#已经下载过一次
    from nltk.corpus import stopwords#使用nltk库>>> 需要提前nltk.download('stopwords')

    stopwords_lists=stopwords.words('english')
    if(type(tokens).__name__=='list'):
        filter_words = [token for token in tokens if token not in stopwords_lists]
        return filter_words
    if(isinstance(tokens,str)):
        return


def word_counter(filter_words):
    """
    :param filter_words: 一维词组
    :return:
    """
    import collections
    return collections.Counter(filter_words)



"""
高频词
"""

def wordfreq_analysis(all_text,freq=10,mode='phrase'):
    """
    词组和单词不同的分词方式

    """

    tokens_list=nltk_tokenize(sentence_tokenize(all_text))#这种分词方式有问题
    if (mode == 'single'):
        tokens_list = find_token(all_text)

    filters_words=remove_stopwords(tokens_list)
    word_count = word_counter(filters_words)
    word_frequency = list(zip(word_count.keys(), word_count.values()))#将counter输出得到合适的格式方便输出
    word_frequency_sorted = sorted(word_frequency, key=lambda x: x[1], reverse=True)  # 倒序输出词频
    # print(word_frequency_sorted)#输出高频词

    with open('气候峰会领导人发言词频统计(去无意义词）.txt', encoding='utf_8', mode='w+') as f:
        f.write('筛选词频阈值为{}'.format(freq)+'\n')
        for item in word_frequency_sorted:
            f.write(str(item[0])+'\t'+str(item[1])+'\n')
            if (item[1] < freq):  # 如果词频低于10就不统计了
                break


"""
词组（有意义的）频率统计
"""
#wordfreq_analysis(all_text,mode='single')
#wordfreq_analysis(all_text,mode='phase')#词频分析

#手动分句
# sentence_list = text.split('.')#两天的发言总文本
# with open(outfile, encoding='utf_8', mode='w+') as f:
#     for sentence in sentence_list:
#         f.write(sentence + '\n')
#print(sentence_list[100:105])


#word_tokens=nltk_tokenize(sentence_list)#分词器结果



"""
词组（有意义的）频率统计
"""



#删除特殊字符




#扩展缩写词
#可根据需要增加缩写词表
contraction_map={

    "isn't":'is not',
    "aren't":'are not'

}

def expand_contrations(sentence,contrction_map=contraction_map):

    contration_pattern=re.compile('({})'.format('|'.join(contraction_map.keys())))  #匹配
    def expand_match(contraction):
        match=contraction[0]
        first_char=match[0]
        expanded_contraction=contraction_map.get(match)\
            if contraction_map.get(match) \
            else contraction_map.get(match.lower())
        expanded_contraction=first_char+expanded_contraction[1:]
        return expanded_contraction
    expanded_sentence=contration_pattern.sub(expand_match,sentence)
    return expanded_sentence



#测试一下

a="i isn't a pig"

print(expand_contrations(a))


"""

拼写错误检查
一般来书,自动翻译的文本不会出现拼写错误

"""


def remove_repeated_characters(tokens):
    """
    矫正重复字符
    """
    #利用wordnet检查词语是否正确
    from nltk.corpus import wordnet
    repeat_pattern=re.compile(r'(\w*)(\w)\2')
    match_substitution=r'\1\2\3'
    def replace(old_word):
        if wordnet.sysnets(old_word):
            return old_word
        new_word=repeat_pattern.sub(match_substitution,old_word)
        return replace(old_word) if old_word!=new_word else new_word

    return [replace(token) for token in tokens]



#词语切分




"""
关键短语提取
"""
#删除特殊字符
def remove_special_characters(all_text):
    """
    :param all_text:全文字符串
    :return: 清洗特殊符号后的句子列表
    """

    import string
    sentence_list=sentence_tokenize(all_text)#一维句子列表
    pattern=re.compile('[{}]'.format(re.escape(string.punctuation)))#去除特殊字符和符号的正则表达式
    sentence_list=[pattern.sub('',sentence) for sentence in sentence_list]
    return sentence_list


from nltk import word_tokenize

#文本规范化
def normalize_corpus(all_text,lemmatize=False):
    #返回二维的文档矩阵
    normalize_corpus=[]
    text_list=remove_special_characters(all_text)#去掉特殊符号的原始的英文文本列表，较好的输入
    for text in text_list:
        text=expand_contrations(text)
        if(lemmatize):
            pass
        else:
            text=text.lower()
        text=word_tokenize(text)
        normalize_corpus.append(text)
    normalize_corpus=remove_stopwords(normalize_corpus)
    return normalize_corpus



#print(normalize_corpus(all_text))

#计算n元组
import nltk
from gensim import models,corpora
class Extraction():
    def __init__(self,corpus,n=2,limit=10):
        self.corpus=corpus
        self.n=n
        self.limit=limit
        self.sentence_list = sentence_tokenize(self.corpus)

    def flattern_corpus(self):
        return nltk_tokenize(self.sentence_list)

    def compute_ngrams(self,squence):

        return zip(* [squence[index:] for index in range(self.n)])

    def get_top_ngrams(self):
        """
        n元语法高频词提取
        :return:
        """
        squence = self.flattern_corpus()
        squence=remove_stopwords(squence)
        ngrams=self.compute_ngrams(squence)

        ngrams_list=nltk.FreqDist(ngrams)
        sorted_ngrams=sorted(ngrams_list.items(),key=lambda x:x[1],reverse=True)
        sorted_ngrams=sorted_ngrams[0:self.limit]
        res=[(' '.join(text),freq) for text,freq in sorted_ngrams]
        return res

    def get_chunks(self,):
        #获取词块
        pass



















