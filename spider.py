import requests



from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import datatime

"""

关键词：Leaders of China, France, Germany Discuss Climate Issues Via Video Summit


"""
import lxml
import requests
import time
import sys
import progress_bar as PB
import json

YOUTUBE_IN_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&pageToken={pageToken}&videoId={videoId}&key={key}'
YOUTUBE_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&videoId={videoId}&key={key}'
key = 'key'  # 改为自己申请的google api


def commentExtract(videoId, count=-1):
    print("\nComments downloading")
    # 关闭http连接，增加重连次数

    page_info = requests.get(YOUTUBE_LINK.format(videoId=videoId, key=key))
    while page_info.status_code != 200:
        if page_info.status_code != 429:
            print("Comments disabled")
            sys.exit()

        time.sleep(20)
        page_info = requests.get(YOUTUBE_LINK.format(videoId=videoId, key=key))

    page_info = page_info.json()
    # test
    # print(page_info)

    comments = []
    co = 0;
    for i in range(len(page_info['items'])):
        # 对3000赞以上的评论进行保留，可以根据需求更改
        if page_info['items'][i]['snippet']['topLevelComment']['snippet']['likeCount'] >= 3000:
            comments.append(page_info['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
            co += 1
        if co == count:
            PB.progress(co, count, cond=True)
            return comments

    PB.progress(co, count)
    # INFINTE SCROLLING
    while 'nextPageToken' in page_info:
        temp = page_info
        page_info = requests.get(YOUTUBE_IN_LINK.format(videoId=videoId, key=key, pageToken=page_info['nextPageToken']))

        while page_info.status_code != 200:
            time.sleep(20)
            page_info = requests.get(YOUTUBE_IN_LINK.format(videoId=videoId, key=key, pageToken=temp['nextPageToken']))
        page_info = page_info.json()

        for i in range(len(page_info['items'])):
            comments.append(page_info['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
            co += 1
            if co == count:
                PB.progress(co, count, cond=True)
                return comments
        PB.progress(co, count)
    PB.progress(count, count, cond=True)
    print()

    return comments

import training_classifier as tcl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os.path
import pickle
from statistics import mode
from nltk.classify import ClassifierI
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import BigramCollocationFinder as BCF
import itertools
from nltk.classify import NaiveBayesClassifier



def features(words):
	temp = word_tokenize(words)

	words = [temp[0]]
	for i in range(1, len(temp)):
		if(temp[i] != temp[i-1]):
			words.append(temp[i])

	scoreF = BigramAssocMeasures.chi_sq

	#bigram count
	n = 150

	bigrams = BCF.from_words(words).nbest(scoreF, n)

	return dict([word,True] for word in itertools.chain(words, bigrams))

class VoteClassifier(ClassifierI):
	def __init__(self, *classifiers):
		self.__classifiers = classifiers

	def classify(self, comments):
		votes = []
		for c in self.__classifiers:
			v = c.classify(comments)
			votes.append(v)
		con = mode(votes)

		choice_votes = votes.count(mode(votes))
		conf = (1.0 * choice_votes) / len(votes)

		return con, conf

def sentiment(comments):

	if not os.path.isfile('classifier.pickle'):
		tcl.training()

	fl = open('classifier.pickle','rb')
	classifier = pickle.load(fl)
	fl.close()

	pos = 0
	neg = 0
	for words in comments:
		# print(words)
		comment = features(words)
		sentiment_value, confidence = VoteClassifier(classifier).classify(comment)
		if sentiment_value == 'positive':# and confidence * 100 >= 60:
			pos += 1
		else:
			neg += 1


	print ("\nPositive sentiment : ", (pos * 100.0 /len(comments)) )
	print ("\nNegative sentiment : ", (neg * 100.0 /len(comments)) )


import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
def fancySentiment(comments):
	stopword = set(stopwords.words('english') + list(string.punctuation) + ['n\'t'])
	filtered_comments = []
	for i in comments:
		words = word_tokenize(i)
		temp_filter = ""
		for w in words:
			if w not in stopword:
				temp_filter += str(w)
				temp_filter += ' '
		filtered_comments.append(temp_filter)
	filtered_comments_str = ' '.join(filtered_comments)
	sentiment = WordCloud(background_color = 'orange', max_words=100)
	sentiment.generate(filtered_comments_str)

	# with open('cloud.txt','w',encoding='utf-8') as f:
	# 	f.write(str(sentiment.generate(filtered_comments_str)))
	plt.figure()
	plt.imshow(sentiment)
	plt.axis("off")
	plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
	plt.margins(0, 0)
	plt.savefig("final.png",dpi=300)
	plt.show()

