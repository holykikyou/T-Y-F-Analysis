
class AllList():  # 存储所有列表信息的对象
    #中文情感词库
    positive_words_eng = [] #正螚量词
    negative_words_eng = [] #负能量词
    level1_words_eng = [] #程度1
    level2_words_eng = [] #程度2
    level3_words_eng = [] #程度3
    level4_words_eng = [] #程度4
    level5_words_eng = [] #程度5
    level6_words_eng = [] #程度6
    fouding_words_eng = [] #否定词
    #英文
    pass

def getAllList():

    allList = AllList()

    # 情感分析(英文)
    file = open("data/eng/pos.txt", encoding='UTF-8')
    while 1:
        line = file.readline()
        if not line:
            break
        pass
        checkTr = str(line).replace('\n', '')
        allList.positive_words_eng.append(checkTr)

    file = open("data/eng/neg.txt", encoding='UTF-8')
    while 1:
        line = file.readline()
        if not line:
            break
        pass
        checkTr = str(line).replace('\n', '')
        allList.negative_words_eng.append(checkTr)

    file = open("data/eng/level1.txt", encoding='UTF-8')
    while 1:
        line = file.readline()
        if not line:
            break
        pass
        checkTr = str(line).replace('\n', '')
        allList.level1_words_eng.append(checkTr)

    file = open("data/eng/level2.txt", encoding='UTF-8')
    while 1:
        line = file.readline()
        if not line:
            break
        pass
        checkTr = str(line).replace('\n', '')
        allList.level2_words_eng.append(checkTr)

    file = open("data/eng/level3.txt", encoding='UTF-8')
    while 1:
        line = file.readline()
        if not line:
            break
        pass
        checkTr = str(line).replace('\n', '')
        allList.level3_words_eng.append(checkTr)

    file = open("data/eng/level4.txt", encoding='UTF-8')
    while 1:
        line = file.readline()
        if not line:
            break
        pass
        checkTr = str(line).replace('\n', '')
        allList.level4_words_eng.append(checkTr)

    file = open("data/eng/level5.txt", encoding='UTF-8')
    while 1:
        line = file.readline()
        if not line:
            break
        pass
        checkTr = str(line).replace('\n', '')
        allList.level5_words_eng.append(checkTr)

    file = open("data/eng/level6.txt", encoding='UTF-8')
    while 1:
        line = file.readline()
        if not line:
            break
        pass
        checkTr = str(line).replace('\n', '')
        allList.level6_words_eng.append(checkTr)

    file = open("data/eng/fouding.txt", encoding='UTF-8')
    while 1:
        line = file.readline()
        if not line:
            break
        pass
        checkTr = str(line).replace('\n', '')
        allList.fouding_words_eng.append(checkTr)

    return allList