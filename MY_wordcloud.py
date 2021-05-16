import wordcloud
class my_Word_cloud():
    def __init__(self,input_file,output_file):
        self.input_file = input_file
        self.output_file = output_file
        _,_,self.en_text,self.cn_text=self.load_word()

    def load_word(self):
        en_word = []
        cn_word = []
        en_text = ''
        cn_text = ''
        with open(self.input_file, encoding='utf_8', mode='r')as f:
            for line in f.readlines():
                line = line.strip()
                cn_word.append(line.split(' ')[-1])
                en_word.append(line.split(' ')[0:-1])
                cn_text += line.split(' ')[-1] + ' '
                for _ in line.split(' ')[0:-1]:
                    en_text +=_ + ' '



        return en_word, cn_word,en_text.strip('_'), cn_text.strip()
    def draw(self,font_path="msyh.ttc",background_color='white',min_font_size=5):

        c = wordcloud.WordCloud(font_path="msyh.ttc", background_color="white", min_font_size=5)
        c.generate(self.en_text)
        c.to_file('tweet_data/en.png')
        c.generate(self.cn_text)
        c.to_file('tweet_data/cn.png')

w=my_Word_cloud(input_file='tweet_data/贸易代表词云.txt',output_file='tweet_data/test.png')
w.draw()

