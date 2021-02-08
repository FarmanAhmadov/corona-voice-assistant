import requests
import json
import pyttsx3
import speech_recognition as sr
import re


API_KEY = "tJ05WmAEZKfU"
PROJECT_TOKEN = "tT3B6wTjLYVF"
RUN_TOKEN = "tZtXQHTXoiTc"

class Data_API:

    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key":self.api_key
        }
        self.get_data()

    def get_data(self):
        response = requests.get(f"https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data", params = {"api_key":self.api_key})
        self.data = json.loads(response.text)

    def get_total_cases(self):
        for item in self.data["total"]:
            self.total_case = item["value"]
            break
        return self.total_case

    def get_total_deaths(self):
        for item in self.data["total"]:
            if item["name"] == "Deaths:":
                return item["value"]

    def get_total_recovered(self):
        for item in self.data["total"]:
            if item["name"] == "Recovered:":
                return item["value"]

    def get_country_data(self, country):
        for content in self.data["country"]:
            if content["name"].lower() == country.lower():
                return  content
        return "0"

data = Data_API(API_KEY,PROJECT_TOKEN)
# print(data.get_country_data("azerbaijan"))

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
        except LookupError:
            print("I did not understand")
    return said.lower()

def main():
    
    while True:
        speak("Do you want some audio information about COVID-19?(Yes or No)")
        answer = get_audio()
        
        if answer == "yes":
            speak("I am listening to you. Ask question please.")
            
            user_voice = get_audio()
            

            if "cases" in user_voice and "world" in user_voice:
                try:
                    pattern = f"There are {data.get_total_cases()}total cases all over the world."
                    speak(pattern)
                except:
                    speak("Unclear voice pattern")
            elif "deaths" in user_voice and "world" in user_voice:
                try:
                    pattern = f"There are {data.get_total_deaths()}total deaths all over the world."
                    speak(pattern)
                except:
                    speak("Unclear voice pattern")

            elif "recovered" in user_voice and "world" in user_voice:
                try:
                    pattern = f"There are {data.get_total_recovered()}total recovered people all over the world."
                    speak(pattern)
                except:
                    speak("Unclear voice pattern")

            elif "world" not in user_voice and "cases" in user_voice:
                try:
                    country = re.search(r"\w+$").group()
                    case_num = data.get_country_data(country)["total_cases"]
                    pattern = f"There are {case_num} total cases in {country}"
                    speak(pattern)

                except:
                    speak("Unclear voice pattern")

            elif "world" not in user_voice and "deaths" in user_voice:
                try:
                    country = re.search(r"\w+$").group()
                    case_num = data.get_country_data(country)["total_deaths"]
                    pattern = f"There are {case_num} total deaths in {country}"
                    speak(pattern)
                except:
                    speak("Unclear voice pattern")
            
            elif "world" not in user_voice and "cases" in user_voice:
                try:
                    country = re.search(r"\w+$").group()
                    case_num = data.get_country_data(country)["total_recovered"]
                    pattern = f"There are {case_num} total recovered people in {country}"
                    speak(pattern)

                except:
                    speak("Unclear voice pattern")

        else:
            speak("You are out of the program")
            break


main()


