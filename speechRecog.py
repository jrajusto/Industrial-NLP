import speech_recognition as sr
import pyttsx3



def readMicrophone():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=0.2)
        print("Please state your query:")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
        except:
            text = "Could not recognize."
    return text

        
