import requests, webbrowser
from bs4 import BeautifulSoup
import copy
import urllib
import json
import datetime
import os
import random
from num2words import num2words
import wikipedia

def assistant(com):
    com = com.lower()
    rcom = copy.deepcopy(com)

    if com.startswith("google") or com.startswith("Google"):
        com = com.replace("google ", "")
        Web_Search(com,1)
        return rcom

    if com.startswith("search") or com.startswith("Search"):
        com = com.rsplit("for ")
        com = com[1]
        speak("What kind of results do you want?, Web, news, video, shopping")
        com2 = listen()
        if com2 in ["Web","web","results","pages"]:
            Web_Search(com, 1)
        if com2 in ["News", "news", "Breaking news", "breaking news"]:
            Web_Search(com, 2)
        if com2 in ["Video", "video", "Youtube", "youtube"]:
            Web_Search(com, 3)
        if com2.lower() in ["shop", "shopping"]:
            Web_Search(com, 1)
        return rcom

    if com.startswith("play") or com.startswith("Play"):
        com = com.replace("play ", "")
        Web_Search(com, 3)
        return rcom

    elif "weather" in com:
        try:
            com = com.rsplit("in ")
            com = com[1]
            w = weather(com)
            return w
        except:
            return "Sorry! didnt understand, Try asking: What is the weather in Patiala?"


    elif "date" in com or "day" in com or "Date" in com or "Day" in com :
        x = datetime.datetime.now()
        ans = "today is" + x.strftime("%A") + "," + num2words(x.strftime("%d")) + x.strftime("%B") + num2words(
            x.strftime("%Y"))
        return ans

    elif "information" in com or "info" in com:
        try:
            if " on " in com:
                com = com.rsplit(" on ")
                com = com[1]
            elif "about" in com:
                com  = com.replace(" about "," on ")
                com = com.rsplit(" on ")
                com = com[1]
        except:
            print("Could not get information!")
            return
        print(com)
        w = wiki(com)
        return w[:1000]


    else:
        try:
            url = "https://robomatic-ai.p.rapidapi.com/api.php"
            query = com
            payload = "SessionID=RapidAPI1&in={}&op=in&cbid=1&cbot=1&ChatSource=RapidAPI&key=RHMN5hnQ4wTYZBGCF3dfxzypt68rVP".format(
                query)
            headers = {
                'content-type': "application/x-www-form-urlencoded",
                'x-rapidapi-key': "90453fa90emshc6459bcf8c3984ep17a855jsn025e5388d417",
                'x-rapidapi-host': "robomatic-ai.p.rapidapi.com"
            }

            response = requests.request("POST", url, data=payload, headers=headers)

            response = response.json()
            print(response["out"])
            return response["out"]
        except:
            print("PLease try again!")
            return "Please try again"

def Web_Search(search,int):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    query = search
    query = query.replace(' ', '+')
    choice = int
    if choice == 1 :
        URL = f"https://google.com/search?q={query}"
        headers = {"user-agent": USER_AGENT}
        resp = requests.get(URL, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            results = soup.select('.rc a')
            for link in results[:3]:
                actual = link.get('href')
                print(actual)
                webbrowser.open(actual)

    elif choice == 2:
        URL = f"https://google.com/search?q={query}" + "&tbm=nws&"
        headers = {"user-agent": USER_AGENT}
        resp = requests.get(URL, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            results = soup.select('.dbsr a')
            for link in results[:4]:
                actual = link.get('href')
                print(actual)
                webbrowser.open(actual)

    elif choice == 3:
        URL = f"https://google.com/search?q={query}" + "&tbm=vid&"
        print(URL)
        headers = {"user-agent": USER_AGENT}
        resp = requests.get(URL, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            results = soup.select('.rGhul')
            for link in results[:1]:
                actual = link.get('href')
                print(actual)
                webbrowser.open(actual)
    return

def weather(city):
    api_key = "69071fdb03e975dc4806bd5dd2aa2a49"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    city_name = city

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name


    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]

        weather_description = z[0]["description"]
        final_weather = (" Temperature right now is " +
              num2words(int(current_temperature) - 273) + " Degree Celcius," +
              "\n atmospheric pressure (in hPa unit) is " +
              num2words(current_pressure) +","+
              "\n humidity is " +
              num2words(current_humidiy) +"Percent,"
              "\n description  " +
              str(weather_description))
    else:
        final_weather = "City Not Found"
    return final_weather


def wiki(search):
    results = wikipedia.search(search)
    return wikipedia.summary(results[0])


print(assistant("hi"))