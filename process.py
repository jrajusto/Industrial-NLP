import preprocess
from nltk.corpus import wordnet as wn
import nltk
from datetime import date

def getNodes(queryType,parent):
    wordList = []
    tagList = []
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == queryType:
                wList = []
                sList = []
                for i in node:
                    wList.append(i[0])
                    sList.append(i[1])
            wordList.append(wList)
            tagList.append(sList)


    return wordList,tagList

def getCurrentYear():
    currentYear = str(date.today())[0:3]
    return currentYear

def getDate():
    currentDate = str(date.today())
    print(currentDate)
    month = currentDate[5:7]
    year = currentDate[0:4]
    day = currentDate[8:10]
    return year,month,day,currentDate
    