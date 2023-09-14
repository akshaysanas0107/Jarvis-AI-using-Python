import speech_recognition as sr
import wikipedia
import pyttsx3 as speak
import webbrowser
import os
import datetime
import requests
import pywhatkit as kit
import subprocess as sp
from config import WEATHER_APIKEY , NEWS_APIKEY


#To Search onGoogle
def search_google(prompt):
    kit.search(prompt)

#To Search On Wikipedia
def search_wikipedia(prompt):
    result = wikipedia.summary(prompt,sentences=2)
    return result

#To get the IP Address 
def getip():
    res = requests.get('https://api64.ipify.org?format=json').json()
    return res["ip"]

#To get news by Default it gives news about "India"
def getnews(topic="India"):
    # topic = "Cricket"
    news_headlines = []
    res = requests.get(f"https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_APIKEY}").json()
    # print(res)
    articles = res['articles']
    for article in articles:
            news_headlines.append(article["title"])
    # print(news_headlines[:5])
    say(news_headlines[:5])

#To get Weather Report by default it gives weather of "India"
def getweather(location="India"):
    BASE_URL = "http://api.weatherapi.com/v1"
    method = "/current.json"
    LOCATION =location

    URL = BASE_URL+method+"?key="+WEATHER_APIKEY+"&q="+LOCATION

    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        say(f"Its {data['current']['condition']['text']} Weather in {LOCATION} with {data['current']['temp_c']} degree celcius Temperature")

#To say something
def say(text):
    print(f"Jarvis: {text}")
    speak.speak(text)

#To Take command from user
def takecommand():
    print("Listening...")
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        
        try:
            query = r.recognize_google(audio , language="en-in")
            print(f"User said: {query}")
            return query
        except:
            return "Some Error occured"


if __name__ == '__main__':
    say("Hello I am Jarvis AI, How may I assist you?")

    while True:
        query = takecommand()
        if "Exit".lower() in query.lower():
            say("Thank you Sir....Have a nice day..")
            break

        if "How are You".lower() in query.lower():
            say("I am Good, How may I assist you?")
            continue
        
        sites = [["Youtube","https://youtube.com"],["Google","https://google.com"],["Wikipedia","https://wikipedia.com"]]
        for site in sites:
            if f"Open {site[0]} Jarvis".lower() in query.lower():
                say(f"Opening {site[0]} sir..")
                webbrowser.open(site[1])

        if "search on wikipedia".lower() in query.lower():
            prompt=query.lower().split('for')[1]
            result = search_wikipedia(prompt)
            print(result)
            say(result)
            
        elif "search on google".lower() in query.lower():
            prompt=query.lower().split('for')[1]
            search_google(prompt)
            say("Showing Results...")

        # To play Local Music file
        if "Play Music".lower() in query.lower():
            musicpath = "Mahabharat.mp3"
            say("Playing Music..")
            os.startfile(musicpath)
           

        elif "What's time ".lower() in query.lower():
            Time = datetime.datetime.now().strftime("%I:%M:%S")
            say(f"Its {Time} now ")


        elif "open chrome".lower() in query.lower():
            os.system('start chrome')
            
        elif "open notepad".lower() in query.lower():
            os.system('start notepad')

        elif "open Camera".lower() in query.lower():
            sp.run('start microsoft.windows.camera:', shell=True)
        
        elif "open Calculator".lower() in query.lower():
            sp.Popen('calc.exe')

        
        elif "open CMD".lower() in query.lower():
            os.system('start cmd')

        elif "Weather".lower() in query.lower():
            try:
                location = query.lower().split("in")[1]
                getweather(location)
            
            except Exception as e:
                getweather()
        
        elif "News".lower() in query.lower(): 
            try:
                topic = query.lower().split("on")[1]
                getnews(topic)
            
            except Exception as e:
                getnews()

        elif "What's your IP".lower() in query.lower():
            say(getip())


  