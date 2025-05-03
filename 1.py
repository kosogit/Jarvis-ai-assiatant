import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import spacy # type: ignore
from fuzzywuzzy import process
import requests
import subprocess as sp

# Initialize the translator, speech engine, and recognizer
translator = Translator()
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Load spaCy English NLP model
nlp = spacy.load("en_core_web_sm")

# Weather and News API Key (replace with your own OpenWeatherMap API key and NewsAPI key)
WEATHER_API_KEY = ''#add your api
NEWS_API_KEY = ''#add your api
NEWS_API_ENDPOINT = ""#add your site link of news api site 

# Function to listen for Hindi speech
def listen_in_hindi():
    with sr.Microphone() as source: 
        print("Listening ...")
        audio = recognizer.listen(source)
        
        try:
            # Recognize speech using Google Speech Recognition (in Hindi)
            hindi_text = recognizer.recognize_google(audio, language='hi-IN')
            print(f"You said (in Hindi): {hindi_text}")
            return hindi_text
        except Exception as e:
            print("Sorry, I couldn't understand. Please try again.")
            return None

# Function to translate Hindi to English
def translate_to_english(hindi_text):
    translated_text = translator.translate(hindi_text, src='hi', dest='en').text
    print(f"Translated (to English): {translated_text}")
    return translated_text

# Function to load responses from a file and search for a match
def load_responses(file_path):
    responses = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                if ":" in line:
                    command, response = line.strip().split(":", 1)
                    responses[command.strip().lower()] = response.strip()
    except FileNotFoundError:
        print("Error: responses.txt file not found.")
    return responses

# Function to find the closest response from the loaded responses
def get_best_response(user_input, responses):
    best_match = process.extractOne(user_input.lower(), responses.keys())
    if best_match and best_match[1] > 60:  # You can adjust the threshold
        return responses[best_match[0]]
    else:
        return "I'm sorry, I am not that good yet."

# Function to get weather information
def get_weather(city):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
        response = requests.get(url)
        weather_data = response.json()
        
        if weather_data['cod'] == 200:
            temperature = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            return f"The current temperature in {city} is {temperature}°C with {description}."
        else:
            return "Sorry, I couldn't fetch the weather for that city."
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return "Sorry, I couldn't fetch the weather at the moment."

def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)

def get_latest_news():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]    

def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]    

# Function to process commands using NLP (spaCy)
def process_command(english_text, responses):
    # Check if the input contains the word "weather"
    if "weather" in english_text.lower():
        print("Weather request detected.")
        
        # Extract city name after "weather in"
        city = None  # No default city
        if "in" in english_text.lower():
            parts = english_text.lower().split("in")
            if len(parts) > 1:
                city = parts[1].strip()  # Extract city after "in"
        
        # If no city was detected, ask the user for the city name
        if not city:
            return "Please specify the city for the weather."
        
        # Get the weather for the detected city
        weather_info = get_weather(city)
        return weather_info
    elif "open camera" in english_text.lower():
        return "Opening camera", open_camera()
    elif "say a joke" in english_text.lower() or "tell joke" in english_text.lower() or "joke" in english_text.lower():
        return get_random_joke()
    
    # Otherwise, process as a normal query
    response = get_best_response(english_text, responses)
    return response

# Function to convert text to speech
def speak_response(response_text):
    engine.say(response_text)
    engine.runAndWait()

# Main function to run Jarvis
def run_jarvis():
    while True:
        print("Jarvis is listening...")

        # Load responses from the file
        responses = load_responses(r"\Python\jarvis\responses.txt")#make sure all file are in one folder 
    
        if not responses:
            print("No responses file available. Exiting...")
            return
    
        # Listen for Hindi speech
        hindi_text = listen_in_hindi()
        if hindi_text:
            
            english_response = translate_to_english(hindi_text)  # Translate to English
            print("Jarvis (in English):", english_response)  # Print response in console
            
            if english_response.lower() == "stop":
                speak_response("Goodbye!")
                break  # Exit the loop
            
            # Process the command using NLP and fetch the response
            nlp_response = process_command(english_response, responses)
            print("Jarvis says:", nlp_response)  # Print the NLP processed response
            speak_response(nlp_response)  # Respond via voice

# Run Jarvis
run_jarvis()
