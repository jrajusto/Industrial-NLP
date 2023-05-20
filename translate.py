import preprocess
import process as p
import nltk
from word2number import w2n
from nltk.corpus import wordnet as wn
from itertools import chain
from datetime import datetime



parameterList = ['temperature','humidity','smoke','noise','flame','id']
parameterToSQL = {'temperature':'Temperature','humidity':'Humidity','smoke':'Smoke_level','noise':'Noise_level','flame':'Flame_occurence','id':'Machine_id'}
monthList = ['january','february','march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
monthListCap = ['January','February','March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
monthToDayMax = {'1':'31','2':'28','3':'31','4':'30','5':'31','6':'30','7':'31','8':'30','9':'31','10':'30','11':'31','12':'30'}

class Machine:
    def __init__(self,name,minHum,maxHum,minTemp,maxTemp,minNoise,maxNoise,minSmoke,maxSmoke,flame):
        self.name = name
        self.minHumidity = minHum
        self.maxHumidity = maxHum
        self.minTemperature = minTemp
        self.maxTemperature = maxTemp
        self.minSmokeLevel = minSmoke
        self.maxSmokeLevel = maxSmoke
        self.minNoiseLevel = minNoise
        self.maxNoiseLevel = maxNoise
        self.flameOccurence = flame

    def setOptimal(self,name,minHum,maxHum,minTemp,maxTemp,minNoise,maxNoise,minSmoke,maxSmoke,flame):
        self.name = name
        self.minHumidity = minHum
        self.maxHumidity = maxHum
        self.minTemperature = minTemp
        self.maxTemperature = maxTemp
        self.minSmokeLevel = minSmoke
        self.maxSmokeLevel = maxSmoke
        self.minNoiseLevel = minNoise
        self.maxNoiseLevel = maxNoise
        self.flameOccurence = flame


def dateCondition(queryType,pos_tags,clean_tokens,monthDict,currentYear,currentMonth,currentDay,lemmatized_tokens):

    dateList = []
    dateString = ""

    chunk_condition = nltk.RegexpParser(queryType[5])
    chunk_condition = chunk_condition.parse(pos_tags)
    
    dateWordList, dateTagList = p.getNodes("date",chunk_condition)

    print("date word list: ")
    print(dateWordList)

    if dateWordList:
        for wordList in dateWordList:
            if wordList[0].lower() in monthList:
                dateList.append(wordList)
    else:
        for word in clean_tokens:
            if word in monthListCap:
                month = str(monthDict[word])
                dateString = "Date_n_Time > '" + currentYear + "-" + month + "-1 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-" + month + "-" + monthToDayMax[month] + " 23:59:59'"
    #if there are two dates given
    if len(dateList) == 2:
        firstDate = dateList[0]
        secondDate = dateList[1]

        #if the first date contains month and date and the second date contains month,date, and year
        if len(firstDate) == 2 and len(secondDate) == 3:
            secondYear = secondDate[2]
            if monthDict[firstDate[0]] > monthDict[secondDate[0]]: 
                firstYear = secondYear - 1
            else:
                firstYear = secondYear

        #if the first date and second date both contains month, date, and year
        elif len(firstDate) == 3 and len(secondDate) == 3:
            secondYear = secondDate[2]
            firstYear = firstDate[2]
        else:
            secondYear = currentYear
            if monthDict[firstDate[0]] > monthDict[secondDate[0]]: 
                firstYear = secondYear - 1
            else:
                firstYear = secondYear
                
        #YYYY-MM-DD hh: mm: ss.nnn
        dateString = "Date_n_Time > '" + str(firstYear) + "-" + str(monthDict[firstDate[0]]) + "-" +  str(firstDate[1]) + " 00:00:00'AND " + "Date_n_Time < '" + str(secondYear) + "-" + str(monthDict[secondDate[0]]) + "-" + str(secondDate[1]) + " 23:59:59'"
        print(dateString)

    elif len(dateList) == 1:
        theDate = dateList[0]
        if len(theDate) == 3:
            if int(theDate[2]) > 31:
                dateString = "Date_n_Time > '" + str(theDate[2]) + "-" + str(monthDict[theDate[0]]) + "-" +  str(theDate[1]) + " 00:00:00' AND Date_n_Time < '" + str(theDate[2]) + "-" + str(monthDict[theDate[0]]) + "-" +  str(theDate[1]) + " 23:59:59'"
            else:
                dateString = "Date_n_Time > '" + currentYear + "-" + str(monthDict[theDate[0]]) + "-" +  str(theDate[1]) + " 00:00:00' AND Date_n_Time < '" + currentYear + "-" + str(monthDict[theDate[0]]) + "-" +  str(theDate[2]) + " 23:59:59'"


        else:
            dateString = "Date_n_Time > '" + currentYear + "-" + str(monthDict[theDate[0]]) + "-" +  str(theDate[1]) + " 00:00:00' AND Date_n_Time < '" + currentYear + "-" + str(monthDict[theDate[0]]) + "-" +  str(theDate[1]) + " 23:59:59'"

    #if asked for data today
    if 'today' in lemmatized_tokens:
        month = str(currentMonth)
        dateString = "Date_n_Time > '" + currentYear + "-" + currentMonth + "-" + currentDay +" 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-" + currentMonth + "-" + currentDay +" 23:59:59'"

    if 'yesterday' in lemmatized_tokens:
        month = str(currentMonth)
        yesterday = str(int(currentDay)-1)
        dateString = "Date_n_Time > '" + currentYear + "-" + currentMonth + "-" + yesterday +" 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-" + currentMonth + "-" + yesterday +" 23:59:59'"

    #if "past week or past # days"
    chunk_condition = nltk.RegexpParser(queryType[7])
    chunk_condition = chunk_condition.parse(pos_tags)

    datePastListList, datePastTagList = p.getNodes("pastCondition",chunk_condition)
    print("date past list")
    print(datePastListList)
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute
    year = currentYear
    month = currentMonth
    day = currentDay
    minute = current_minute
    hour = current_hour

    if datePastListList: 
        for datePastList in datePastListList:

            pastWordList = ["past","last",'previous']

            if datePastList[0] in pastWordList:
                if len(datePastList) == 2:
                    numberVal = 1
                    timeValue = datePastList[1]
                else:
                    numberVal = int(w2n.word_to_num(datePastList[1]))
                    timeValue = datePastList[2]

                if timeValue == "day":
                    if int(currentDay) <= numberVal:
                        if int(currentMonth) == 1:
                            month = "12"
                            year = str(int(currentYear)-1)
                        else: 

                            month = str(int(currentMonth)-1)
                            year = currentYear
                        day = int(monthToDayMax[month]) - (numberVal - int(currentDay))
                    else:
                        month = str(currentMonth)
                        day = str(int(currentDay) - numberVal)
                        year = currentYear
                        
                    dateString = "Date_n_Time > '" + year + "-" + month + "-" + str(day) +" 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-" + currentMonth + "-" + str(int(currentDay)) +" 23:59:59'"
                
                if timeValue == "hour":
                    

                    if current_hour <= numberVal:
                        if int(currentDay) == 1:
                            day = str(int(monthToDayMax[str(int(currentMonth)-1)]))
                            if int(currentMonth) == 1:
                                month = "12"
                                year = str(int(currentYear)-1)
                            else: 

                                month = str(int(currentMonth)-1)
                                year = currentYear

                        else: 
                            
                            day = str(int(currentDay)-1)
                            month = str(currentMonth)
                            year = currentYear
                        
                        hour = str(24 - (numberVal - current_hour))
                    else:
                        day = currentDay
                        hour = str(current_hour-numberVal)
                        month = str(currentMonth)
                        year = str(currentYear)

                    dateString = "Date_n_Time > '" + year + "-" + month + "-" + day +" " + hour + ":00:00'" + " AND Date_n_Time < '" + currentYear + "-" + currentMonth + "-" + currentDay +" " + str(current_hour) + ":59:59'"
                
                if timeValue == "minute":
                    current_minute = datetime.now().minute

                    if current_minute <= numberVal:
                        if int(current_hour) == 0:
                            hour = "23"
                            if int(currentDay) == 1:
                                day = str(int(monthToDayMax[str(int(currentMonth)-1)]))
                                if int(currentMonth) == 1:
                                    month = "12"
                                    year = str(int(currentYear)-1)
                                else: 

                                    month = str(int(currentMonth)-1)
                                    year = currentYear

                            else: 
                                
                                day = str(int(currentDay)-1)
                                month = str(currentMonth)
                                year = currentYear
                            
                        else: 
                            hour = str(current_hour-1)
                            day = str(currentDay)
                            month = str(currentMonth)
                            year = currentYear
                        
                        minute = str(60 - (numberVal - current_minute))
                    else:
                        day = currentDay
                        hour = str(current_hour)
                        minute = str(current_minute - numberVal)
                        month = str(currentMonth)
                        

                    dateString = "Date_n_Time > '" + year + "-" + month + "-" + day +" " + hour + ":"+ minute + ":00'" + " AND Date_n_Time < '" + currentYear + "-" + currentMonth + "-" + currentDay +" " + str(current_hour) + ":59:59'"
                

                if timeValue == "week":
                    day = numberVal * 7
                    if int(currentDay) <= day:
                        if int(currentMonth) == 1:
                            month = "12"
                            year = str(int(currentYear)-1)
                        else:
                            month = str(int(currentMonth)-1)
                            year = currentYear
                        day = int(monthToDayMax[month]) - (day - int(currentDay))
                    else:
                        month = str(currentMonth)
                        year = currentYear
                        day = int(currentDay) - day

                    dateString = "Date_n_Time > '" + year + "-" + month + "-" + str(day) +" 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-" + currentMonth + "-" + str(currentDay) +" 23:59:59'"

                if timeValue == "year":
                    year = str(int(currentYear)-1)
                    dateString = "Date_n_Time > '" + year + "-01-01 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-12-31 23:59:59'"

                if timeValue == "month":
                    if int(currentMonth) <= numberVal:
                        year = str(int(currentYear)-1)
                        month = str(12 - (numberVal-int(currentMonth)))
                    else:
                        month = str(int(currentMonth)-numberVal)
                        year = currentYear

                    dateString = "Date_n_Time > '" + year + "-" + month + "-1 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-" + str(int(currentMonth)-1) + "-" + monthToDayMax[str(currentMonth)] +" 23:59:59'"


                


    #finding query with this month or last month
    chunk_month = nltk.RegexpParser(queryType[3])
    chunk_month = chunk_month.parse(pos_tags)
    monthQueryList, monthQueryTagList = p.getNodes("monthQuery",chunk_month)

    print('Month query list:')
    print(monthQueryList)
    
    if monthQueryList:
        for monthQuery in monthQueryList:
            if 'month' in monthQuery:
                for monthQueryPhrase in monthQuery:
                    if monthQueryPhrase == 'this': 
                        dateString = "Date_n_Time > '" + currentYear + "-" + currentMonth + "-1 00:00:00'" + " AND Date_n_Time < '" + currentYear + "-" + currentMonth + "-" + monthToDayMax[currentMonth] + " 23:59:59'"
                 
    return dateString

def optimalCondition(sqlQuery,tokens,clean_tokens,parameterList,optimalMachine,entries,specificBool,currentYear,currentMonth,currentDay,finalQueries,queryType,pos_tags,monthDict,lemmatized_tokens):
    
    whereOnce = False
    andDelay = 0
    #add conditions of optimal machine
    for word in tokens:
        if word in parameterList and parameterToSQL[word] not in entries:
            if whereOnce == False:
                sqlQuery = sqlQuery + "WHERE ("
                whereOnce = True
            
            if andDelay == 1:
                sqlQuery = sqlQuery + " OR"
                print('pass')

            if andDelay == 0:
                andDelay = 1
            
            if word == "temperature":
                sqlQuery = sqlQuery + " Temperature < " + str(optimalMachine.minTemperature) + " Temperature > " + str(optimalMachine.maxTemperature)
                entries.append('Temperature')

            elif word == "humidity":
                sqlQuery = sqlQuery + " Humidity < " + str(optimalMachine.minHumidity) + " Humidity > " + str(optimalMachine.maxHumidity)
                entries.append('Humidity')

            elif word == "smoke":
                sqlQuery = sqlQuery + " Smoke_level < " + str(optimalMachine.minSmokeLevel) + " Smoke_level > " + str(optimalMachine.maxSmokeLevel)
                entries.append('Smoke_level')

            elif word == "noise":
                sqlQuery = sqlQuery + " Noise_level < " + str(optimalMachine.minNoiseLevel) + " Noise_level > " + str(optimalMachine.maxNoiseLevel)
                entries.append('Noise_level')

            elif word == "flame":
                sqlQuery = sqlQuery + " Flame_occurence != " + str(optimalMachine.flameOccurence) 
                entries.append('Flame_occurence')
            

    if whereOnce:
        sqlQuery = sqlQuery + ")"

    if specificBool != True:
        sqlQuery = sqlQuery + " WHERE (Temperature < " + str(optimalMachine.minTemperature) + " OR Temperature > " + str(optimalMachine.maxTemperature) + " OR Humidity < " + str(optimalMachine.minHumidity) + " OR Humidity > " + str(optimalMachine.maxHumidity) + " OR Smoke_level < " +str(optimalMachine.minSmokeLevel) + " OR Smoke_level > " +str(optimalMachine.maxSmokeLevel) + " OR Noise_level < " + str(optimalMachine.minNoiseLevel) + " OR Noise_level > " + str(optimalMachine.maxNoiseLevel) + " OR Flame_occurence < " +str(optimalMachine.flameOccurence)+")"
        entries.append('Temperature')
        entries.append('Humidity')
        entries.append('Smoke_level')
        entries.append('Flame_occurence')
        entries.append('Noise_level')
        
        
    
    dateString = dateCondition(queryType,pos_tags,clean_tokens,monthDict,currentYear,currentMonth,currentDay,lemmatized_tokens)
    if dateString != "":
        sqlQuery = sqlQuery + " AND " + dateString

    finalQueries.append(sqlQuery)      
    return finalQueries



def convertToSql(query,optimalMachine1,optimalMachine2,optimalMachine3,optimalMachine4,machineList):
    currentYear,currentMonth,currentDay,fullDate = p.getDate()
    #initial entries list
    entries = ['ID','Machine_id','Date_n_Time']

    machineDict = {                                                                                                                        
        optimalMachine1.name:"sensor_node_1_tb",
        optimalMachine2.name:"sensor_node_2_tb",
        optimalMachine3.name:"sensor_node_3_tb",
        optimalMachine4.name:"sensor_node_4_tb"
    }

    #list of the months


    #dictionary of the months with number equivalent
    monthDict = {'January':1,'February':2,'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
    graphBool = False
    compareBool = False
    averageBool = False
    maximumBool = False
    minimumBool = False
    countBool = False

    query = query.lower()
    tokens = preprocess.tokenize(query)

    for i in range(len(tokens)):
        if tokens[i] in monthList:
            tokens[i] = tokens[i].capitalize()

    clean_tokens = preprocess.remove_stop_words(tokens)
    lemmatized_tokens = preprocess.lemmatize(clean_tokens)
    if 'fahrenheit' in lemmatized_tokens:
        lemmatized_tokens = preprocess.fahrenheitToCelsius(lemmatized_tokens)
    lemmatized_tokens = preprocess.replaceNum(lemmatized_tokens)

    for token in lemmatized_tokens:
        if token == 'mean' or token == 'average':
            lemmatized_tokens.remove(token)
            averageBool = True
        if token == 'max' or token == 'maximum':
            lemmatized_tokens.remove(token)
            maximumBool = True
        if token == 'count':
            lemmatized_tokens.remove(token)
            countBool = True
        if token == 'min' or token == 'minimum':
            minimumBool = True


    pos_tags = preprocess.pos_tagging(lemmatized_tokens)

    print('original')
    orig_pos_tags = preprocess.pos_tagging(tokens)

    queryType = []
    queryType.append(r"command: {<NNP|JJ|VB|NN|WP|VBP><NN|DT|VBP|VBZ|RB|NNS>*<NN|JJ|VBZ|VBG>}") #Show the smoke level of the cutting machine
    queryType.append(r"condition: {<NN|JJ|VBD><JJR|JJ|NN|IN|RBR|VBP|VBZ|NNP>?<CD><CD>?}") #humidity is greater than 5
    queryType.append(r"conjuctions: {<CC>}") #AND OR
    queryType.append(r"monthQuery: {<DT|JJ|IN><NN>}") #this month or last 
    queryType.append(r"withincondition: {<NN|JJ|VBD>?<IN><CD><CD>}") #temperature is within 
    queryType.append(r"date: {<NNP><CD><CD>?}") #from january 5 to january 30
    queryType.append(r"numParam: {<JJR|JJ|NN|IN|RBR|VBP|VBZ><CD><NN|JJ|VBD>?<NN|JJ|VBD>}") #greater than 30 percent humidity
    queryType.append(r"pastCondition: {<IN|JJ><CD>?<NN>}") #past 7 days
    queryType.append(r"twoCondition: {<NN|JJ|VBD>?<JJR|VBP><JJ><CD>}") # parameter? less/greater than or equal to


    
    #parse the query acording to query type 1
    chunk_parserTest1 = nltk.RegexpParser(queryType[0])
    chunk_parserTest1 = chunk_parserTest1.parse(pos_tags)
    
    
    #test 1 - with action
    command,test1Tags = p.getNodes("command",chunk_parserTest1)
    print("command")
    print(command)
    command = command[0]

    commandWords = []
    finalString = None
    finalQueries = []

    machineNames = []

    synonyms = wn.synsets('graph')
    graphSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('compare')
    compareSynonyms =set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('show')
    showSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('get')
    getSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('output')
    outputSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('optimal')
    optimalSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('good')
    goodSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('greater')
    greaterSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('above')
    aboveSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('more')
    moreSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('below')
    belowSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))

    synonyms = wn.synsets('equal')
    equalSynonyms = set(chain.from_iterable([word.lemma_names() for word in synonyms]))





    #cutoff the end of the phrase with machine name
    for word in command:
        commandWords.append(word)
        if word in machineList:
            break
    
    command = commandWords

    optimalBool = True
    
    
    
    if(len(command) > 0):
        #check if show, get or graph is in the tokens
        for word in command:
            if((word in showSynonyms) or (word in getSynonyms) or (word in graphSynonyms) or (word in compareSynonyms) or (word in outputSynonyms) or (word == "list")or (word == "plot")or (word == "what")or (word == "retrieve")):
                optimalBool = False
                break
        if not optimalBool:
            for word in command:
                if((word not in showSynonyms) and (word not in getSynonyms) and (word not in graphSynonyms) and (word not in compareSynonyms) and (word not in outputSynonyms)and (word != "check")and (word != "list")and (word != "plot")and (word != "what")and (word != "retrieve")):
                    command.remove(word)
                else:
                    break
    print("command: ")
    print(command)



    operationList = ['greater','le','equal']
    adjectiveList = ['optimal','good']

    #getting dates
    
    print("Current Date")
    print(p.getDate())


    if(optimalBool):
        
        print('running optimal test')
            
        
        for word in lemmatized_tokens:
    
            if word in machineList:
                entries = ['ID','Machine_id','Date_n_Time']
                
                print("found the machine")
                machineNames.append(word)

                sqlQuery = "SELECT ID, Date_n_Time, Machine_id"
                specificBool = False
                for word in lemmatized_tokens:
                    if word in parameterList:
                        specificBool = True
                        sqlQuery = sqlQuery + ", " + parameterToSQL[word] 
                if not specificBool:
                    for word in lemmatized_tokens:
                        if word in parameterList:
                            specificBool = True
                            sqlQuery = sqlQuery + ", " + parameterToSQL[word] 

                if machineNames[0] == optimalMachine1.name:
                    optimalMachine = optimalMachine1
                    if specificBool:
                        sqlQuery= sqlQuery + " FROM sensor_node_1_tb "
                    else:
                        sqlQuery= "SELECT * FROM sensor_node_1_tb "
                        
                elif machineNames[0] == optimalMachine2.name:
                    optimalMachine = optimalMachine2
                    if specificBool:
                        sqlQuery= sqlQuery + " FROM sensor_node_2_tb "
                    else:
                        sqlQuery= "SELECT * FROM sensor_node_2_tb "
                elif machineNames[0] == optimalMachine3.name:
                    optimalMachine = optimalMachine3
                    if specificBool:
                        sqlQuery= sqlQuery + " FROM sensor_node_3_tb "
                    else:
                        sqlQuery= "SELECT * FROM sensor_node_3_tb "
                elif machineNames[0] == optimalMachine4.name:
                    optimalMachine = optimalMachine4
                    if specificBool:
                        sqlQuery= sqlQuery + " FROM sensor_node_4_tb "
                    else:
                        sqlQuery= "SELECT * FROM sensor_node_4_tb "
                
                finalQueries = optimalCondition(sqlQuery,tokens,clean_tokens,parameterList,optimalMachine,entries,specificBool,currentYear,currentMonth,currentDay,finalQueries,queryType,pos_tags,monthDict,lemmatized_tokens)


        if "all machines" in query or not machineNames:
            for machine in machineList:
                machineNames.append(machine)

            for count in range (1,5):
                sqlQuery = "SELECT * FROM sensor_node_"+str(count)+ "_tb "
                whereOnce = False
                andDelay = 0

                if count == 1:
                    optimalMachine = optimalMachine1
                elif count == 2:
                    optimalMachine = optimalMachine2
                elif count == 3:
                    optimalMachine = optimalMachine3
                elif count == 4:
                    optimalMachine = optimalMachine4


                #add conditions of optimal machine
                specificBool = False
                entries = ['ID','Machine_id','Date_n_Time']
                finalQueries = optimalCondition(sqlQuery,tokens,clean_tokens,parameterList,optimalMachine,entries,specificBool,currentYear,currentMonth,currentDay,finalQueries,queryType,pos_tags,monthDict,lemmatized_tokens)

#------------------------------------------------------------------------------------------------------------------------------------
    #finding action
    elif(len(command) > 0):

    
            if(command[0] in graphSynonyms or command[0] == "plot"):
                graphBool = True
                
            if(command[0] in compareSynonyms):
                compareBool = True

            
            #finding between condition
            chunk_condition = nltk.RegexpParser(queryType[4])
            chunk_condition = chunk_condition.parse(pos_tags)
            
            ################## between parameter condition #######################
            withinParameterWordList, withinParameterTagWordList = p.getNodes("withincondition",chunk_condition)
            print("within Parameter word list: ")
            print(withinParameterWordList)

            if withinParameterWordList:
                withinParameterWordList = withinParameterWordList[0]
                if withinParameterWordList[0] in parameterList:
                    withinParameter =  withinParameterWordList[0]
                    withinParameterExist = True
                    withinParameterWordList.pop(0)
                    withinParameterWordList.pop(0)
                    withinValues = withinParameterWordList
                else:
                    withinParameterExist = False
                    withinParameterWordList.pop(0)
                    withinParameterWordList.pop(0)
                    withinValues = withinParameterWordList
                        
            #finding condition
            chunk_condition = nltk.RegexpParser(queryType[1])
            chunk_condition = chunk_condition.parse(pos_tags)
            
            parameterWordList, parameterTagList = p.getNodes("condition",chunk_condition)
            print("Parameter word list: ")
            print(parameterWordList)

            
            conditionString = []
            paramFound = False
            ############### for num parameter ###########################
            chunk_numParam = nltk.RegexpParser(queryType[6])
            chunk_numParam = chunk_numParam.parse(pos_tags)

            chunkParamList, chunkParamTags = p.getNodes("numParam",chunk_numParam)
            print("numParam:")
            print(chunkParamList)
            
            numParamBool = False
            numParamList = []
            if chunkParamList:
                for chunkParam in chunkParamList:
                    lenChunkParam = len(chunkParam)
                    conditionString = []
                    if chunkParam[lenChunkParam-1] in parameterList:
                        numParamList.append(chunkParam)
                    
                    print("numparambool")
                    print(numParamBool)

            
            if (len(numParamList) == 1 and 'and' not in tokens) or (len(numParamList)>1 and 'and' in tokens) :
                numParamBool = True
                for numParam in numParamList:
                    wordList = numParam
                    lenChunkParamList = len(numParam)
                    if lenChunkParamList == 4:
                        if wordList[0] == operationList[0] or wordList[0] in greaterSynonyms or wordList[0] in aboveSynonyms or wordList[0] in moreSynonyms:
                            conditionString.append(parameterToSQL[wordList[3]] +' > ' + str(w2n.word_to_num(wordList[1])))
                        elif wordList[0] == operationList[0] or wordList[0] in belowSynonyms:
                            conditionString.append(parameterToSQL[wordList[3]] +' < ' + str(w2n.word_to_num(wordList[1])))
                        elif wordList[0] == operationList[0] or wordList[0] in equalSynonyms:
                            conditionString.append(parameterToSQL[wordList[3]] +' = ' + str(w2n.word_to_num(wordList[1])))
                        else:
                            conditionString.append(parameterToSQL[wordList[3]] +' = ' + str(w2n.word_to_num(wordList[1])))
                    elif lenChunkParamList == 5:
                        if wordList[4] in parameterList:
                            if wordList[0] == operationList[0] or wordList[0] in greaterSynonyms or wordList[0] in aboveSynonyms or wordList[0] in moreSynonyms:
                                conditionString.append(parameterToSQL[wordList[4]] +' > ' + str(w2n.word_to_num(wordList[1])))
                            elif wordList[0] == operationList[0] or wordList[0] in belowSynonyms:
                                conditionString.append(parameterToSQL[wordList[4]] +' < ' + str(w2n.word_to_num(wordList[1])))
                            elif wordList[0] == operationList[0] or wordList[0] in equalSynonyms:
                                conditionString.append(parameterToSQL[wordList[4]] +' = ' + str(w2n.word_to_num(wordList[1])))
                            else:
                                conditionString.append(parameterToSQL[wordList[4]] +' = ' + str(w2n.word_to_num(wordList[1])))
                    elif lenChunkParamList == 3:
                        if wordList[2] in parameterList:
                            if wordList[0] == operationList[0] or wordList[0] in greaterSynonyms or wordList[0] in aboveSynonyms or wordList[0] in moreSynonyms:
                                conditionString.append(parameterToSQL[wordList[2]] +' > ' + str(w2n.word_to_num(wordList[1])))
                            elif wordList[0] == operationList[0] or wordList[0] in belowSynonyms:
                                conditionString.append(parameterToSQL[wordList[2]] +' < ' + str(w2n.word_to_num(wordList[1])))
                            elif wordList[0] == operationList[0] or wordList[0] in equalSynonyms:
                                conditionString.append(parameterToSQL[wordList[2]] +' = ' + str(w2n.word_to_num(wordList[1])))
                            else:
                                conditionString.append(parameterToSQL[wordList[2]] +' = ' + str(w2n.word_to_num(wordList[1])))
                    elif lenChunkParamList == 2:
                        conditionString.append(parameterToSQL[wordList[2]] +' = ' + str(w2n.word_to_num(wordList[1])))
                    elif lenChunkParamList == 1:
                        conditionString.append(parameterToSQL[wordList[1]] +' = ' + str(w2n.word_to_num(wordList[0])))

            ############## for greater/less than or equal to ##################
            chunk_condition = nltk.RegexpParser(queryType[8])
            chunk_condition = chunk_condition.parse(pos_tags)

            chunkTwoConditionList, chunkTwoConditionTags = p.getNodes("twoCondition",chunk_condition)     
            twoConditionBool = False
            for wordList in chunkTwoConditionList:
                if len(wordList) == 3:
                    if wordList[0] in parameterList:
                        twoConditionBool = True
                        if wordList[1] == operationList[0] or wordList[1] in greaterSynonyms or wordList[1] in aboveSynonyms or wordList[1] in moreSynonyms:
                            conditionString.append(parameterToSQL[wordList[0]] +' >= ' + str(w2n.word_to_num(wordList[2])))
                        elif wordList[1] == operationList[1] or wordList[1] in belowSynonyms:
                            conditionString.append(parameterToSQL[wordList[0]] +' <= ' + str(w2n.word_to_num(wordList[2])))
                    else:
                        for i in lemmatized_tokens:
                                if i in parameterList:
                                    parameterUsed = i
                                    break
                        if wordList[1] == operationList[0] or wordList[1] in greaterSynonyms or wordList[1] in aboveSynonyms or wordList[1] in moreSynonyms:
                            conditionString.append(parameterToSQL[parameterUsed] +' >= ' + str(w2n.word_to_num(wordList[2])))
                        elif wordList[1] == operationList[1] or wordList[1] in belowSynonyms:
                            conditionString.append(parameterToSQL[parameterUsed] +' <=' + str(w2n.word_to_num(wordList[2])))
                elif len(wordList) == 2:
                    for i in lemmatized_tokens:
                                if i in parameterList:
                                    parameterUsed = i
                                    break
                    if wordList[0] == operationList[0] or wordList[0] in greaterSynonyms or wordList[0] in aboveSynonyms or wordList[0] in moreSynonyms:
                        conditionString.append(parameterToSQL[parameterUsed] +' >= ' + str(w2n.word_to_num(wordList[2])))
                        twoConditionBool = True
                    elif wordList[0] == operationList[1] or wordList[0] in belowSynonyms:
                        conditionString.append(parameterToSQL[parameterUsed] +' <=' + str(w2n.word_to_num(wordList[2])))
                        twoConditionBool = True

          

            print("condition string: ")
            print(conditionString)

            if not withinParameterWordList and not numParamBool and not twoConditionBool:
                for wordList in parameterWordList:
                

                    if wordList[0] in parameterList:
                        paramFound = True
                        if wordList[1] == operationList[0] or wordList[1] in greaterSynonyms or wordList[1] in aboveSynonyms or wordList[1] in moreSynonyms:
                            conditionString.append(parameterToSQL[wordList[0]] +' > ' + str(w2n.word_to_num(wordList[2])))
                        elif wordList[1] == operationList[1] or wordList[1] in belowSynonyms:
                            conditionString.append(parameterToSQL[wordList[0]] +' < ' + str(w2n.word_to_num(wordList[2])))
                        elif wordList[1] == operationList[2] or wordList[1] in equalSynonyms:
                            conditionString.append(parameterToSQL[wordList[0]] +' = ' + str(w2n.word_to_num(wordList[2])))
                        else:
                            conditionString.append(parameterToSQL[wordList[0]] +' = ' + str(w2n.word_to_num(wordList[1])))
                        print("condition string: ")
                        print(conditionString)
                        #condition name is not given
                    elif len(wordList) == 3:
                        if wordList[2].isdigit() and wordList[1] in parameterList:
                            paramFound = True
                            parameterUsed = command[1]

                            if wordList[1] == operationList[0] or wordList[1] in greaterSynonyms or wordList[1] in aboveSynonyms or wordList[1] in moreSynonyms:
                                conditionString.append(parameterToSQL[parameterUsed] +' > ' + str(w2n.word_to_num(wordList[2])))
                            elif wordList[1] == operationList[1] or wordList[1] in belowSynonyms:
                                conditionString.append(parameterToSQL[parameterUsed] +' < ' + str(w2n.word_to_num(wordList[2])))
                            elif wordList[1] == operationList[2] or wordList[1] in equalSynonyms:
                                conditionString.append(parameterToSQL[parameterUsed] +' = ' + str(w2n.word_to_num(wordList[2])))
                            else:
                                conditionString.append(parameterToSQL[parameterUsed] +' = ' + str(w2n.word_to_num(wordList[1])))

                        if wordList[2].isdigit():
                            for i in lemmatized_tokens:
                                if i in parameterList:
                                    parameterUsed = i
                                    break
                            if wordList[1] == operationList[0] or wordList[1] in greaterSynonyms or wordList[1] in aboveSynonyms or wordList[1] in moreSynonyms:
                                conditionString.append(parameterToSQL[parameterUsed] +' > ' + str(w2n.word_to_num(wordList[2])))
                            elif wordList[1] == operationList[1] or wordList[1] in belowSynonyms:
                                conditionString.append(parameterToSQL[parameterUsed] +' < ' + str(w2n.word_to_num(wordList[2])))
                            elif wordList[1] == operationList[2] or wordList[1] in equalSynonyms:
                                conditionString.append(parameterToSQL[parameterUsed] +' = ' + str(w2n.word_to_num(wordList[2])))
                            
            print("condition string: ")
            print(conditionString)

            

            #finding conjunctions
            chunk_conjuctions = nltk.RegexpParser(queryType[2])
            chunk_conjuctions = chunk_conjuctions.parse(orig_pos_tags)

            conjunctionList,conJunctionTags = p.getNodes("conjuctions",chunk_conjuctions)


            #finding datetime
            print("current year")
            print(currentYear)
            dateString = dateCondition(queryType,pos_tags,clean_tokens,monthDict,currentYear,currentMonth,currentDay,lemmatized_tokens)


            
            #find machine name in test1 words
            for word in lemmatized_tokens:
                if word in machineList:
                    machineNames.append(word)
            
            if not machineNames:
                for machine in machineList:
                    machineNames.append(machine)

            #final string      
            commaSet = False
            if (command[1] == "everything" or ((command[1] == 'all' and "all machines" not in query))):
                entries.append('Temperature')
                entries.append('Humidity')
                entries.append('Smoke_level')
                entries.append('Flame_occurence')
                entries.append('Noise_level')
                
                
                finalString = "SELECT * FROM " + machineDict[machineNames[0]]
            else:
                finalString = "SELECT ID,Machine_id, Date_n_Time" 
                showSpecified = False
                for word in command:
                    
                    if word in parameterList:
                        entries.append(parameterToSQL[word])
                        finalString = finalString + ", "
                        finalString = finalString + parameterToSQL[word]
                        showSpecified = True

                        


                        if withinParameterWordList:
                            if withinParameterExist == False:
                                withinParameter = parameterToSQL[word]
                
                #if paramter shown not specified
                if showSpecified == False:
                    for word in tokens:
                        if word in parameterList:
                            entries.append(parameterToSQL[word])
                            finalString = finalString + ", "
                            finalString = finalString + parameterToSQL[word]


 
                try:
                    finalString = finalString + " FROM " + machineDict[machineNames[0]]
                except:
                    print("***machine not found***")
                

            if withinParameterWordList:
                conditionString.append(withinParameter + " > " + withinValues[0] + " AND " + withinParameter + " < " + withinValues[1])


            #see if dateString exist
            print("Date string:")
            print(dateString)

            if(len(conditionString) > 0 or dateString != ""):
                finalString = finalString + " WHERE "
            
            if(len(conditionString) > 0):
                finalString = finalString + "("

            conjunctionListNum = 0
            for i in range(len(conditionString)):
                finalString = finalString + conditionString[i] + " "
                if i < len(conditionString) - 1 and len(withinParameterWordList) < 1:
                    finalString = finalString  + conjunctionList[conjunctionListNum][0].upper() + " "
                conjunctionListNum = conjunctionListNum + 1

            if(len(conditionString) > 0):
                finalString = finalString + ") "

            if dateString != "":
                if(len(conditionString) == 0):
                    finalString = finalString + dateString
                else:
                    finalString = finalString + " AND " + dateString
            
            print(finalString)
            finalQueries.append(finalString)
            if len(machineNames) > 1:
                for i in range(1,len(machineNames)):
                    finalQueries.append(finalString.replace(machineDict[machineNames[0]],machineDict[machineNames[i]]))
    print("headings")
    print(entries)
    
    #if showing no condition
    if len(entries) == 2:
        raise Exception('no condition given')

    countValue = []
    for i in lemmatized_tokens:
        if i.isdigit():
            countValue.append(float(i))

    
    #returns the final translated string, and the headings of the condition
    print(finalQueries, entries,graphBool,compareBool,optimalBool, averageBool,maximumBool,minimumBool,countBool,countValue,machineNames)
    return finalQueries, entries,graphBool,compareBool,optimalBool,averageBool, maximumBool,minimumBool,countBool,countValue,machineNames