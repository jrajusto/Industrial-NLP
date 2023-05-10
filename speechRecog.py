import speech_recognition as sr



def readMicrophone():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please state your query:")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
        except:
            text = "Could not recognize."
    return text

        
