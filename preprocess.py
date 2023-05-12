
from nltk.tokenize import word_tokenize
from nltk.stem import wordnet
from nltk.util import ngrams
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re #using re.compile
import nltk
from num2words import num2words
import os
from nltk.tag import StanfordPOSTagger



def lowercase(query):
    lowercase_tokens = []
    for word in query:
        lowercase_tokens.append(word.lower())

    print('lowercase tokens: ')
    print(lowercase_tokens)
    return lowercase_tokens

def tokenize(query):
    tokenized_query = word_tokenize(query)
    print('tokenized query: ')
    print(tokenized_query)
    return tokenized_query

def numToWord(tokens):
    for token in tokens:
        if token.isdigit():
            token = str(num2words(token))
            print(token)
    print(tokens)

    return tokens

def lemmatize(tokens):
    word_lem=WordNetLemmatizer()
    lemmatized_tokens = []
    for word in tokens:
        lemmatized_tokens.append(word_lem.lemmatize(word))
    print("lemmatized tokens:")
    print(lemmatized_tokens)
    return lemmatized_tokens

def remove_stop_words(tokens):
    custom_stopwords = stopwords.words('english')
    custom_stopwords.remove('above')
    custom_stopwords.remove('this')
    custom_stopwords.remove('below')
    custom_stopwords.remove('all')
    custom_stopwords.append('plant')
    custom_stopwords.append('quality')
    custom_stopwords.append('level')
    custom_stopwords.append('moisture')
    custom_stopwords.append('core')
    custom_stopwords.append('intensity')
    custom_stopwords.append('reading')
    custom_stopwords.append('respect')
    custom_stopwords.remove('between')
    custom_stopwords.remove('more')
    custom_stopwords.append('generate')
    custom_stopwords.append('me')
    custom_stopwords.remove('what')

    new_tokens = [word for word in tokens if word not in custom_stopwords]
    
    #removes punctuations
    punctuation = re.compile(r'[-.?!,:;()|]')
    post_punctuation = []
    for words in new_tokens:
        word = punctuation.sub("",words)
        if len(word)> 0 :
            post_punctuation.append(word)

    print("removed stop words")
    print(post_punctuation)
    return post_punctuation
    

def pos_tagging(tokens):
    
    java_path = "/usr/lib/jvm/default-java/bin"
    os.environ['JAVAHOME'] = java_path
    stanford_dir = "/home/cpe124-group4/nlpThesis/stanford-postagger"
    model_path = stanford_dir + "/models/english-bidirectional-distsim.tagger"
    jar_path = stanford_dir + "/stanford-postagger.jar"
    tagger = StanfordPOSTagger(model_path, path_to_jar=jar_path)
    print("pos tags:")
    tags = tagger.tag(tokens)
    print(tags)

    return tags

def create_ngram(lower_tokens):
    print (list(ngrams(lower_tokens,4)))
    return list(ngrams(lower_tokens,4))

def replaceNum(tokens):
    for i in tokens:
        if len(i) >= 2:
            if i[-2]+i[-1] == 'st':
                num = i.replace('st','')
                if num.isdigit(): 
                    tokens = [num if item == i else item for item in tokens]

            if i[-2]+i[-1] == 'nd':
                num = i.replace('nd','')
                if num.isdigit(): 
                    tokens = [num if item == i else item for item in tokens]

            if i[-2]+i[-1] == 'rd':
                num = i.replace('rd','')
                if num.isdigit(): 
                    tokens = [num if item == i else item for item in tokens]

            if i[-2]+i[-1] == 'th':
                num = i.replace('th','')
                if num.isdigit(): 
                    tokens = [num if item == i else item for item in tokens]


    return tokens

def fahrenheitToCelsius(tokens):
    for i in tokens:
        if i.isdigit():
            num = (str(int((int(i)-32)*5/9)))
            tokens = [num if item == i else item for item in tokens]
        if i == 'fahrenheit':
            tokens = ['celsius' if item == i else item for item in tokens]

    print(tokens)
    print("^^^")

    return tokens



