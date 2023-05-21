from ast import Lambda
from tkinter import *
import tkinter
from turtle import heading
import speechRecog as s
import threading
import mysql.connector
from tkinter import ttk
import translate
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import csv
import time
outputRowCount = 0

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

machineList = []

with open('optimalParameters.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    
    for row in csv_reader:
        if line_count != 0:
            machineList.append(row[0])
        if line_count == 1:
            optimalMachine1 = Machine(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
        if line_count == 2:
            optimalMachine2 = Machine(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
        if line_count == 3:
            optimalMachine3 = Machine(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
        if line_count == 4:
            optimalMachine4 = Machine(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
        line_count = line_count + 1
    csv_file.close()


#optimal conditions for the machines



averageList = []

SQLtoParameter = {'Temperature':'temperature','Humidity':'humidity','Noise_level':'noise level','Smoke_level':'smoke level','Flame_occurence':'occurence of flame'}

def editOptimal(name,minHum,maxHum,minTemp,maxTemp,minNoise,maxNoise,minSmoke,maxSmoke,flame,node):
    df = pd.read_csv("optimalParameters.csv")
    global machineList

    if node == 1:
        optimalMachine1.setOptimal(name,minHum,maxHum,minTemp,maxTemp,minNoise,maxNoise,minSmoke,maxSmoke,flame)
        machineList[0] = name

    elif node == 2:
        optimalMachine2.setOptimal(name,minHum,maxHum,minTemp,maxTemp,minNoise,maxNoise,minSmoke,maxSmoke,flame)
        machineList[1] = name

    elif node == 3:
        optimalMachine3.setOptimal(name,minHum,maxHum,minTemp,maxTemp,minNoise,maxNoise,minSmoke,maxSmoke,flame)
        machineList[2] = name

    elif node == 4:
        optimalMachine4.setOptimal(name,minHum,maxHum,minTemp,maxTemp,minNoise,maxNoise,minSmoke,maxSmoke,flame)
        machineList[3] = name

    df.loc[node-1,'Name'] = name
    df.loc[node-1,'minHumidity'] = minHum
    df.loc[node-1,'maxHumidity'] = maxHum
    df.loc[node-1,'minTemperature'] = minTemp
    df.loc[node-1,'maxTemperature'] = maxTemp
    df.loc[node-1,'minSmoke_level'] = minSmoke
    df.loc[node-1,'maxSmoke_level'] = maxSmoke
    df.loc[node-1,'minNoise_level'] = minNoise
    df.loc[node-1,'maxNoise_level'] = maxNoise
    df.loc[node-1,'Flame_occurence'] = flame

    df.to_csv("optimalParameters.csv", index=False)
    


def openOptimalWindow():
    optimalWindow = Toplevel(root)

    optimalWindow.title('Optimal conditions')
    optimalWindowFrame = LabelFrame(optimalWindow,text="Optimal Conditions")
    optimalWindowFrame.pack()

    #for sensor node 1
    sensornode1Frame = LabelFrame(optimalWindowFrame,text="Sensor Node 1")
    sensornode1Frame.grid(column=0,row=0,ipadx=5)

    sensornode1Name = Label(sensornode1Frame,text="Name")
    sensornode1Name.grid(row=0,column=0)
    sensornode1NameInput = Entry(sensornode1Frame,width=10)
    sensornode1NameInput.grid(row=0,column=1)
    sensornode1NameInput.insert(0,optimalMachine1.name)

    sensornode1TemperatureText = Label(sensornode1Frame,text="Temperature (C)")
    sensornode1TemperatureText.grid(row=1,column=0)
    sensornode1minTemperatureInput = Entry(sensornode1Frame,width=10)
    sensornode1minTemperatureInput.grid(row=1,column=1)
    sensornode1minTemperatureInput.insert(0,optimalMachine1.minTemperature)
    sensornode1ToTemperatureText = Label(sensornode1Frame,text=" - ")
    sensornode1ToTemperatureText.grid(row=1,column=2)
    sensornode1maxTemperatureInput = Entry(sensornode1Frame,width=10)
    sensornode1maxTemperatureInput.grid(row=1,column=3)
    sensornode1maxTemperatureInput.insert(0,optimalMachine1.maxTemperature)
    

    sensornode1HumidityText = Label(sensornode1Frame,text="Humidity")
    sensornode1HumidityText.grid(row=2,column=0)
    sensornode1minHumidityInput = Entry(sensornode1Frame,width=10)
    sensornode1minHumidityInput.grid(row=2,column=1)
    sensornode1minHumidityInput.insert(0,optimalMachine1.minHumidity)
    sensornode1ToHumidityText = Label(sensornode1Frame,text=" - ")
    sensornode1ToHumidityText.grid(row=2,column=2)
    sensornode1maxHumidityInput = Entry(sensornode1Frame,width=10)
    sensornode1maxHumidityInput.grid(row=2,column=3)
    sensornode1maxHumidityInput.insert(0,optimalMachine1.maxHumidity)

    sensornode1NoiseText = Label(sensornode1Frame,text="Noise level")
    sensornode1NoiseText.grid(row=3,column=0)
    sensornode1minNoiseInput = Entry(sensornode1Frame,width=10)
    sensornode1minNoiseInput.grid(row=3,column=1)
    sensornode1minNoiseInput.insert(0,optimalMachine1.minNoiseLevel)
    sensornode1ToNoiseText = Label(sensornode1Frame,text=" - ")
    sensornode1ToNoiseText.grid(row=3,column=2)
    sensornode1maxNoiseInput = Entry(sensornode1Frame,width=10)
    sensornode1maxNoiseInput.grid(row=3,column=3)
    sensornode1maxNoiseInput.insert(0,optimalMachine1.maxNoiseLevel)

    sensornode1SmokeText = Label(sensornode1Frame,text="Smoke level")
    sensornode1SmokeText.grid(row=4,column=0)
    sensornode1minSmokeInput = Entry(sensornode1Frame,width=10)
    sensornode1minSmokeInput.grid(row=4,column=1)
    sensornode1minSmokeInput.insert(0,optimalMachine1.minSmokeLevel)
    sensornode1ToSmokeText = Label(sensornode1Frame,text=" - ")
    sensornode1ToSmokeText.grid(row=4,column=2)
    sensornode1maxSmokeInput = Entry(sensornode1Frame,width=10)
    sensornode1maxSmokeInput.grid(row=4,column=3)
    sensornode1maxSmokeInput.insert(0,optimalMachine1.maxSmokeLevel)

    sensornode1FireText = Label(sensornode1Frame,text="Occurence of fire")
    sensornode1FireText.grid(row=5,column=0)
    sensornode1FireInput = Entry(sensornode1Frame,width=10)
    sensornode1FireInput.grid(row=5,column=1)
    sensornode1FireInput.insert(0,optimalMachine1.flameOccurence)


    sensornode1button = Button(sensornode1Frame,text="Edit",width=10,command = lambda: editOptimal(sensornode1NameInput.get(),sensornode1minHumidityInput.get(),sensornode1minHumidityInput.get(),sensornode1minTemperatureInput.get(),sensornode1maxTemperatureInput.get(),sensornode1minNoiseInput.get(),sensornode1maxNoiseInput.get(),sensornode1minSmokeInput.get(),sensornode1maxSmokeInput.get(),sensornode1FireInput.get(),1))
    sensornode1button.grid(row=6,column=1)

    #for sensor node 2
    sensornode2Frame = LabelFrame(optimalWindowFrame,text="Sensor Node 2")
    sensornode2Frame.grid(column=1,row=0,ipadx=5)

    sensornode2Name = Label(sensornode2Frame,text="Name")
    sensornode2Name.grid(row=0,column=0)
    sensornode2NameInput = Entry(sensornode2Frame,width=10)
    sensornode2NameInput.grid(row=0,column=1)
    sensornode2NameInput.insert(0,optimalMachine2.name)

    sensornode2TemperatureText = Label(sensornode2Frame,text="Temperature (C)")
    sensornode2TemperatureText.grid(row=1,column=0)
    sensornode2minTemperatureInput = Entry(sensornode2Frame,width=10)
    sensornode2minTemperatureInput.grid(row=1,column=1)
    sensornode2minTemperatureInput.insert(0,optimalMachine2.minTemperature)
    sensornode2ToTemperatureText = Label(sensornode2Frame,text=" - ")
    sensornode2ToTemperatureText.grid(row=1,column=2)
    sensornode2maxTemperatureInput = Entry(sensornode1Frame,width=10)
    sensornode2maxTemperatureInput.grid(row=1,column=3)
    sensornode2maxTemperatureInput.insert(0,optimalMachine2.maxTemperature)
    
    

    sensornode2HumidityText = Label(sensornode2Frame,text="Humidity")
    sensornode2HumidityText.grid(row=2,column=0)
    sensornode2minHumidityInput = Entry(sensornode2Frame,width=10)
    sensornode2minHumidityInput.grid(row=2,column=1)
    sensornode2minHumidityInput.insert(0,optimalMachine2.minHumidity)
    sensornode2ToHumidityText = Label(sensornode2Frame,text=" - ")
    sensornode2ToHumidityText.grid(row=2,column=2)
    sensornode2maxHumidityInput = Entry(sensornode2Frame,width=10)
    sensornode2maxHumidityInput.grid(row=2,column=3)
    sensornode2maxHumidityInput.insert(0,optimalMachine2.maxHumidity)

    sensornode2NoiseText = Label(sensornode2Frame,text="Noise level")
    sensornode2NoiseText.grid(row=3,column=0)
    sensornode2minNoiseInput = Entry(sensornode2Frame,width=10)
    sensornode2minNoiseInput.grid(row=3,column=1)
    sensornode2minNoiseInput.insert(0,optimalMachine2.minNoiseLevel)
    sensornode2ToNoiseText = Label(sensornode2Frame,text=" - ")
    sensornode2ToNoiseText.grid(row=3,column=2)
    sensornode2maxNoiseInput = Entry(sensornode2Frame,width=10)
    sensornode2maxNoiseInput.grid(row=3,column=3)
    sensornode2maxNoiseInput.insert(0,optimalMachine2.maxNoiseLevel)

    sensornode2SmokeText = Label(sensornode2Frame,text="Smoke level")
    sensornode2SmokeText.grid(row=4,column=0)
    sensornode2minSmokeInput = Entry(sensornode2Frame,width=10)
    sensornode2minSmokeInput.grid(row=4,column=1)
    sensornode2minSmokeInput.insert(0,optimalMachine2.minSmokeLevel)
    sensornode2ToSmokeText = Label(sensornode2Frame,text=" - ")
    sensornode2ToSmokeText.grid(row=4,column=2)
    sensornode2maxSmokeInput = Entry(sensornode2Frame,width=10)
    sensornode2maxSmokeInput.grid(row=4,column=3)
    sensornode2maxSmokeInput.insert(0,optimalMachine2.maxSmokeLevel)

    sensornode2FireText = Label(sensornode2Frame,text="Occurence of fire")
    sensornode2FireText.grid(row=5,column=0)
    sensornode2FireInput = Entry(sensornode2Frame,width=10)
    sensornode2FireInput.grid(row=5,column=1)
    sensornode2FireInput.insert(0,optimalMachine2.flameOccurence)


    sensornode2button = Button(sensornode2Frame,text="Edit",width=10,command = lambda: editOptimal(sensornode2NameInput.get(),sensornode2minHumidityInput.get(),sensornode2minHumidityInput.get(),sensornode2minTemperatureInput.get(),sensornode2maxTemperatureInput.get(),sensornode2minNoiseInput.get(),sensornode2maxNoiseInput.get(),sensornode2minSmokeInput.get(),sensornode2maxSmokeInput.get(),sensornode2FireInput.get(),2))
    sensornode2button.grid(row=6,column=1)


    #for sensor node 3
    sensornode3Frame = LabelFrame(optimalWindowFrame,text="Sensor Node 3")
    sensornode3Frame.grid(column=0,row=1,ipadx=5)

    sensornode3Name = Label(sensornode3Frame,text="Name")
    sensornode3Name.grid(row=0,column=0)
    sensornode3NameInput = Entry(sensornode3Frame,width=10)
    sensornode3NameInput.grid(row=0,column=1)
    sensornode3NameInput.insert(0,optimalMachine3.name)

    sensornode3TemperatureText = Label(sensornode3Frame,text="Temperature (C)")
    sensornode3TemperatureText.grid(row=1,column=0)
    sensornode3minTemperatureInput = Entry(sensornode3Frame,width=10)
    sensornode3minTemperatureInput.grid(row=1,column=1)
    sensornode3minTemperatureInput.insert(0,optimalMachine3.minTemperature)
    sensornode3ToTemperatureText = Label(sensornode3Frame,text=" - ")
    sensornode3ToTemperatureText.grid(row=1,column=2)
    sensornode3maxTemperatureInput = Entry(sensornode1Frame,width=10)
    sensornode3maxTemperatureInput.grid(row=1,column=3)
    sensornode3maxTemperatureInput.insert(0,optimalMachine3.maxTemperature)
    
    

    sensornode3HumidityText = Label(sensornode3Frame,text="Humidity")
    sensornode3HumidityText.grid(row=2,column=0)
    sensornode3minHumidityInput = Entry(sensornode3Frame,width=10)
    sensornode3minHumidityInput.grid(row=2,column=1)
    sensornode3minHumidityInput.insert(0,optimalMachine3.minHumidity)
    sensornode3ToHumidityText = Label(sensornode3Frame,text=" - ")
    sensornode3ToHumidityText.grid(row=2,column=2)
    sensornode3maxHumidityInput = Entry(sensornode3Frame,width=10)
    sensornode3maxHumidityInput.grid(row=2,column=3)
    sensornode3maxHumidityInput.insert(0,optimalMachine3.maxHumidity)

    sensornode3NoiseText = Label(sensornode3Frame,text="Noise level")
    sensornode3NoiseText.grid(row=3,column=0)
    sensornode3minNoiseInput = Entry(sensornode3Frame,width=10)
    sensornode3minNoiseInput.grid(row=3,column=1)
    sensornode3minNoiseInput.insert(0,optimalMachine3.minNoiseLevel)
    sensornode3ToNoiseText = Label(sensornode3Frame,text=" - ")
    sensornode3ToNoiseText.grid(row=3,column=2)
    sensornode3maxNoiseInput = Entry(sensornode3Frame,width=10)
    sensornode3maxNoiseInput.grid(row=3,column=3)
    sensornode3maxNoiseInput.insert(0,optimalMachine3.maxNoiseLevel)

    sensornode3SmokeText = Label(sensornode3Frame,text="Smoke level")
    sensornode3SmokeText.grid(row=4,column=0)
    sensornode3minSmokeInput = Entry(sensornode3Frame,width=10)
    sensornode3minSmokeInput.grid(row=4,column=1)
    sensornode3minSmokeInput.insert(0,optimalMachine3.minSmokeLevel)
    sensornode3ToSmokeText = Label(sensornode3Frame,text=" - ")
    sensornode3ToSmokeText.grid(row=4,column=2)
    sensornode3maxSmokeInput = Entry(sensornode3Frame,width=10)
    sensornode3maxSmokeInput.grid(row=4,column=3)
    sensornode3maxSmokeInput.insert(0,optimalMachine3.maxSmokeLevel)

    sensornode3FireText = Label(sensornode3Frame,text="Occurence of fire")
    sensornode3FireText.grid(row=5,column=0)
    sensornode3FireInput = Entry(sensornode3Frame,width=10)
    sensornode3FireInput.grid(row=5,column=1)
    sensornode3FireInput.insert(0,optimalMachine3.flameOccurence)


    sensornode3button = Button(sensornode3Frame,text="Edit",width=10,command = lambda: editOptimal(sensornode3NameInput.get(),sensornode3minHumidityInput.get(),sensornode3minHumidityInput.get(),sensornode3minTemperatureInput.get(),sensornode3maxTemperatureInput.get(),sensornode3minNoiseInput.get(),sensornode3maxNoiseInput.get(),sensornode3minSmokeInput.get(),sensornode3maxSmokeInput.get(),sensornode3FireInput.get(),3))
    sensornode3button.grid(row=6,column=1)

    #for sensor node 4
    sensornode4Frame = LabelFrame(optimalWindowFrame,text="Sensor Node 4")
    sensornode4Frame.grid(column=1,row=1,ipadx=5)

    sensornode4Name = Label(sensornode4Frame,text="Name")
    sensornode4Name.grid(row=0,column=0)
    sensornode4NameInput = Entry(sensornode4Frame,width=10)
    sensornode4NameInput.grid(row=0,column=1)
    sensornode4NameInput.insert(0,optimalMachine4.name)

    sensornode4TemperatureText = Label(sensornode4Frame,text="Temperature (C)")
    sensornode4TemperatureText.grid(row=1,column=0)
    sensornode4minTemperatureInput = Entry(sensornode4Frame,width=10)
    sensornode4minTemperatureInput.grid(row=1,column=1)
    sensornode4minTemperatureInput.insert(0,optimalMachine4.minTemperature)
    sensornode4ToTemperatureText = Label(sensornode4Frame,text=" - ")
    sensornode4ToTemperatureText.grid(row=1,column=2)
    sensornode4maxTemperatureInput = Entry(sensornode1Frame,width=10)
    sensornode4maxTemperatureInput.grid(row=1,column=3)
    sensornode4maxTemperatureInput.insert(0,optimalMachine4.maxTemperature)
    
    

    sensornode4HumidityText = Label(sensornode4Frame,text="Humidity")
    sensornode4HumidityText.grid(row=2,column=0)
    sensornode4minHumidityInput = Entry(sensornode4Frame,width=10)
    sensornode4minHumidityInput.grid(row=2,column=1)
    sensornode4minHumidityInput.insert(0,optimalMachine4.minHumidity)
    sensornode4ToHumidityText = Label(sensornode4Frame,text=" - ")
    sensornode4ToHumidityText.grid(row=2,column=2)
    sensornode4maxHumidityInput = Entry(sensornode4Frame,width=10)
    sensornode4maxHumidityInput.grid(row=2,column=3)
    sensornode4maxHumidityInput.insert(0,optimalMachine4.maxHumidity)

    sensornode4NoiseText = Label(sensornode4Frame,text="Noise level")
    sensornode4NoiseText.grid(row=3,column=0)
    sensornode4minNoiseInput = Entry(sensornode4Frame,width=10)
    sensornode4minNoiseInput.grid(row=3,column=1)
    sensornode4minNoiseInput.insert(0,optimalMachine4.minNoiseLevel)
    sensornode4ToNoiseText = Label(sensornode4Frame,text=" - ")
    sensornode4ToNoiseText.grid(row=3,column=2)
    sensornode4maxNoiseInput = Entry(sensornode4Frame,width=10)
    sensornode4maxNoiseInput.grid(row=3,column=3)
    sensornode4maxNoiseInput.insert(0,optimalMachine4.maxNoiseLevel)

    sensornode4SmokeText = Label(sensornode4Frame,text="Smoke level")
    sensornode4SmokeText.grid(row=4,column=0)
    sensornode4minSmokeInput = Entry(sensornode4Frame,width=10)
    sensornode4minSmokeInput.grid(row=4,column=1)
    sensornode4minSmokeInput.insert(0,optimalMachine4.minSmokeLevel)
    sensornode4ToSmokeText = Label(sensornode4Frame,text=" - ")
    sensornode4ToSmokeText.grid(row=4,column=2)
    sensornode4maxSmokeInput = Entry(sensornode4Frame,width=10)
    sensornode4maxSmokeInput.grid(row=4,column=3)
    sensornode4maxSmokeInput.insert(0,optimalMachine4.maxSmokeLevel)

    sensornode4FireText = Label(sensornode4Frame,text="Occurence of fire")
    sensornode4FireText.grid(row=5,column=0)
    sensornode4FireInput = Entry(sensornode4Frame,width=10)
    sensornode4FireInput.grid(row=5,column=1)
    sensornode4FireInput.insert(0,optimalMachine4.flameOccurence)


    sensornode4button = Button(sensornode4Frame,text="Edit",width=10,command = lambda: editOptimal(sensornode4NameInput.get(),sensornode4minHumidityInput.get(),sensornode4minHumidityInput.get(),sensornode4minTemperatureInput.get(),sensornode4maxTemperatureInput.get(),sensornode4minNoiseInput.get(),sensornode4maxNoiseInput.get(),sensornode4minSmokeInput.get(),sensornode4maxSmokeInput.get(),sensornode4FireInput.get(),4))
    sensornode4button.grid(row=6,column=1)




#get query from textbox
def getInputQuery():
    global query
    global queryView
    global outputQuerytext
    global outputAnswer
    global tableFrame

    query = inputQuery.get()

    try:
        outputQuerytext
    except:
        print('DNE')
    else:
        outputQuerytext.grid_forget()

    printQuery()
        
#shows the input query to be translated on screen
def printQuery():
    global query
    global outputQuerytext

    outputQuerytext = Label(outputQueryFrame,padx=5,pady=5,text=query)
    outputQuerytext.grid(row=0,column=0)
    continueButton = Button(outputQueryFrame,text="Continue",command=translateQuery,padx=10)
    continueButton.grid(row=0,column=1)

def printAnswer(answer):
    global outputAnswer
    global outputAnswerFrame
    

    outputAnswer = Label(outputAnswerFrame,text=answer)
    outputAnswer.pack()

    

#gets voice input from user
def speak():
    global speakFrame
    speakFrame = LabelFrame(firstWindow,padx=5,pady=5)
    speakFrame.pack(padx=10,pady=10)
    speakingLabel = Label(speakFrame,text="Start speaking now...")
    speakingLabel.pack()

    #threading.Thread(target=readmic).start()
    readmic()
   
#get voice input from mic
def readmic():

    global query
    global speakingBox
    query = s.readMicrophone()
    print(query)
    global speakFrame
    speakFrame.pack_forget()
    
    try:
        outputQuerytext
    except:
        print('DNE')
    else:
        outputQuerytext.grid_forget()

    printQuery()
 
    speakFrame.destroy()
    print('pass2')

#create table from sql output
def createTable(output,machineName):
    global canvasFrame
    global outputRowCount 
    outputMachineDataFrame = LabelFrame(canvasFrame,text = machineName)
    outputMachineDataFrame.grid(row=outputRowCount,column=0)
    
    outputRowCount= outputRowCount + 1

    
    global tableFrame

    tableFrame = Frame(outputMachineDataFrame)
    tableFrame.pack(side=tkinter.LEFT,padx=1)

    headings = ttk.Treeview(tableFrame,columns=tuple(headingList),show="headings")
    headings.grid(row=0, column=0)
    for i in headingList:
        if i == 'Machine_id':
            headings.heading(i, text = 'M. ID')
        elif i == 'Flame_occurence':
            headings.heading(i, text = 'Flame')
        elif i == 'Noise_level':
            headings.heading(i, text = 'Noise')
        elif i == 'Smoke_level':
            headings.heading(i, text = 'Smoke')
        else:
            headings.heading(i, text = i)
    for i in output:
        headings.insert('','end',values=i)

    for i in headingList:
        if i == 'ID':
            headings.column(i, width=30, anchor=CENTER)
        elif i == 'Date_n_Time':
            headings.column(i, width=120, anchor=CENTER)
        elif i == 'Machine_id':
            headings.column(i, width=50, anchor=CENTER)
        elif i == 'Flame_occurence':
            headings.column(i, width=50, anchor=CENTER)
        elif i == 'Temperature':
            headings.column(i, width=80, anchor=CENTER)
        elif i == 'Smoke_level':
            headings.column(i, width=50, anchor=CENTER)
        elif i == 'Noise_level':
            headings.column(i, width=50, anchor=CENTER)
        elif i == 'Humidity':
            headings.column(i, width=50, anchor=CENTER) 
        else:
            headings.column(i, width=120, anchor=CENTER)



    scrollbar = ttk.Scrollbar(tableFrame, orient=tkinter.VERTICAL, command=headings.yview)
    headings.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')


#translate the query to sql query and execupte
def translateQuery():
    global sqlQuery
    global headingList
    global graphBool
    global optimalBool
    global compareBool
    global machineNames
    global outputAnswer
    global tableFrame
    global machineNo
    global outputDataFrame
    global outputAnswerFrame
    global outputRowCount
    global outputCanvas 
    global canvasFrame
    
    
    try:
        outputAnswerFrame
    except:
        print('DNE')
        
        
    else:
        outputAnswerFrame.pack_forget()

    outputAnswerFrame = LabelFrame(firstWindow,padx=5,pady=5,text='Answer')
    outputAnswerFrame.pack(anchor=W)
    
   
    try:
        outputDataFrame
    except:
        print("")
    else:
        outputDataFrame.pack_forget()
        outputRowCount = 0
    
    outputDataFrame = Frame(firstWindow)
    outputDataFrame.pack()

    
    
    outputCanvas = Canvas(outputDataFrame,width=500,height=250)
    outputCanvas.pack(side=LEFT, fill = BOTH, expand = 1)
    scrollbarMachine = ttk.Scrollbar(outputDataFrame, orient=VERTICAL, command=outputCanvas.yview)
    scrollbarMachine.pack(side=RIGHT,fill=Y)

    outputCanvas.configure(yscrollcommand=scrollbarMachine.set)
    outputCanvas.bind('<Configure>',lambda e: outputCanvas.configure(scrollregion=outputCanvas.bbox("all")))
    
    canvasFrame = Frame(outputCanvas)
    outputCanvas.create_window((0,0),window=canvasFrame,anchor="nw")


    

    sqlQueries,headingList,graphBool,compareBool,optimalBool,averageBool,maximumBool,minimumBool,countBool,countValue,machineNames = translate.convertToSql(query,optimalMachine1,optimalMachine2,optimalMachine3,optimalMachine4,machineList)
    
    machineNo = 0
    for sqlQuery in sqlQueries:
        
        myCursor.execute(sqlQuery)
        output = myCursor.fetchall()
        #if output exist, create the table
        if output:
            createTable(output,machineNames[machineNo])
            
        print(headingList)
        print('Graph state')
        print(graphBool)

        if graphBool:

            if output:
                df = pd.DataFrame (output, columns = headingList)
                headingList.remove('ID')
                headingList.remove('Machine_id')
                headingList.remove('Date_n_Time')
                

                if len(headingList) > 1:
                    figure, axis = plt.subplots(len(headingList))

                    headingNo = 0
                    for heading in headingList:
                        axis[headingNo].plot(df['Date_n_Time'],df[heading])
                        axis[headingNo].set_title(heading + " of " + machineNames[machineNo])
                        headingNo = headingNo + 1
                else:
                    plt.plot(df['Date_n_Time'],df[headingList[0]])
                    plt.title(headingList[0] + " of " + machineNames[machineNo])

                plt.tight_layout(h_pad=0.55)
                plt.show()

                headingList.insert(0,'ID')
                headingList.insert(2,'Machine_id')
                headingList.insert(1,'Date_n_Time')
                
            else:
                printAnswer("There is no data to show.")

        machineNo = machineNo + 1

        if compareBool:
            
            df = pd.DataFrame (output, columns = headingList)
            print(headingList)
            headingList.remove('ID')
            headingList.remove('Machine_id')
            headingList.remove('Date_n_Time')
            

            headingNo = 0
            for heading in headingList:
                plt.plot(df['Date_n_Time'],df[heading])
                #axis[headingNo].set_title(heading)
                headingNo = headingNo + 1

            plt.tight_layout(h_pad=0.55)
            plt.legend(headingList)
            plt.show()

            headingList.insert(0,'ID')
            headingList.insert(2,'Machine_id')
            headingList.insert(1,'Date_n_Time')
            

        if optimalBool:
            #if output is empty
            if not output:
                printAnswer("The machines has mantained optimal condition.")
            else:
                printAnswer("The machines has not mantained optimal condition in these occasions.")

            print(output)

        
        if averageBool:
            df = pd.DataFrame (output, columns = headingList)
            headingList.remove('ID')
            headingList.remove('Machine_id')
            headingList.remove('Date_n_Time')
            print(headingList)

            outputSentence = ""
            
            for heading in headingList:
                outputSentence = outputSentence + "The average " + SQLtoParameter[heading] + " is " + str(round(df[heading].mean(),2)) + ". "
            printAnswer(outputSentence)

        if maximumBool:
            df = pd.DataFrame (output, columns = headingList)
            headingList.remove('ID')
            headingList.remove('Machine_id')
            headingList.remove('Date_n_Time')
            print(headingList)

            headingNo = 0
            outputSentence = ""
            for heading in headingList:
                outputSentence = outputSentence + "The maximum " + SQLtoParameter[heading] + " is " + str(df[heading].max()) + ". "
            printAnswer(outputSentence)


        if minimumBool:
            df = pd.DataFrame (output, columns = headingList)
            headingList.remove('ID')
            headingList.remove('Machine_id')
            headingList.remove('Date_n_Time')
            print(headingList)

            headingNo = 0
            outputSentence = ""
            for heading in headingList:
                outputSentence = outputSentence + "The minimum " + SQLtoParameter[heading] + " is " + str(df[heading].min()) + ". "
            printAnswer(outputSentence)

        

        if countBool:
            df = pd.DataFrame (output, columns = headingList)
            headingList.remove('ID')
            headingList.remove('Machine_id')
            headingList.remove('Date_n_Time')
            print(headingList)
            headingNo = 0
            outputSentence = ""
            for heading in headingList:
                outputSentence = outputSentence + "The occurence of " + SQLtoParameter[heading] + " is " + str(df[heading].value_counts()[countValue]) + ". "
                headingNo = headingNo + 1
            printAnswer(outputSentence)


    

#database initialization
try:
    db = mysql.connector.connect(host="localhost",user="root",password="mapua",database="sensornetwork2")
except:
    print("MySQL connection is not found.")
else:
    #gui initialization
    root = Tk()
    root.title("Prototype")
    #root.geometry("750x400")
    root.tk.call('tk','scaling',0.9)
    myCursor = db.cursor()

    #global variables
    queryView = False

    #first window
    firstWindow = LabelFrame(root)
    firstWindow.grid(row=0,column=0)

    #second window
    secondWindow = LabelFrame(root,text="Optimal conditions")
    secondWindow.grid(row=0,column=1,sticky='n')

    #showOptimal button
    showOptimal = Button(secondWindow,text="Show optimal conditions",command=openOptimalWindow)
    showOptimal.pack()

    #input query frame
    inputQueryFrame = LabelFrame(firstWindow,text="Input Query",padx=5,pady=5)
    inputQueryFrame.pack(anchor=W)

    #input query text box
    inputQuery = Entry(inputQueryFrame,width=50)
    inputQuery.grid(row=0,column=0)

        #query = "Show the core temperature from the grapes machines where humidity is greater than 20 and temperature is less than 30 in december 2 to december 7 2021"
        #query = "Show the core temperature from the grapes machines where humidity is greater than 20 in december 2 to december 7 2021"
        #query = "Show the core temperature from the grapes machines where humidity is greater than 20 in december 2 2021 to december 7 2021
        #query = "Show all from the grapes machines" 
        #query = "Has the tomato machines maintain optimal codition last month"
        #query = "Show the core temperature from the corn machines"
        #query = "Show the core temperature from the corn machines this month"
        #query = "Graph the core temperature and humidity from the corn machines"
        #query = "Compare the core temperature and humidity from the corn machines"
        #query = "Show humidity from corn within 30 and 60"
        #query = "Show humidity from corn where temperature is between 30 and 60"
        #query = "Has the tomato and corn machine reached optimal conditions"
        #query = "Show humidity from corn greater 30 degrees temperature"

    inputQuery.insert(0,"Show the flame occurence from the printer")

    #enter button
    enterButton = Button(inputQueryFrame,text="Enter",command=getInputQuery,padx=10)
    enterButton.grid(row=0,column=1)


    #speak query frame
    
    speakQueryFrame = LabelFrame(firstWindow,padx=5,pady=5,text='Speak Query')
    speakQueryFrame.pack(anchor=W)


    speakLabel = Label(speakQueryFrame,text = "Press the button and state your query")
    speakLabel.grid(row=1,column=0)

    #speak button
    speakButton = Button(speakQueryFrame, text = "Speak",command=speak, padx=10)
    speakButton.grid(row=1,column=1)
    

    #Output query frame
    outputQueryFrame = LabelFrame(firstWindow,padx=5,pady=5,text='You entered the query')
    outputQueryFrame.pack(anchor=W)

    #Output answer frame
    outputAnswerFrame = LabelFrame(firstWindow,padx=5,pady=5,text='Answer')
    outputAnswerFrame.pack(anchor=W)
    outputAnswerFrame.size()


    #Output data graph
    outputDataGraph = LabelFrame(firstWindow,text = 'Output Data Graph')
    outputDataGraph.pack()

    

    root.mainloop()