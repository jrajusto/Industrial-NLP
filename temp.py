
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
