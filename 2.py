import speech_recognition as sr
import pyttsx3
from deep_translator import GoogleTranslator # type: ignore
import os
import openai # type: ignore
from datetime import datetime

# Replace with your OpenAI API Key
openai.api_key =""#add your open ai api 

# Initialize
recognizer = sr.Recognizer()
engine = pyttsx3.init()
RESPONSE_DIR = "/responses.txt"

# Create response folder if not exists
if not os.path.exists(RESPONSE_DIR):
    os.makedirs(RESPONSE_DIR)

# Speech to Text
def listen_in_hindi():
    with sr.Microphone() as source:
        print("Listening ...")
        audio = recognizer.listen(source)
        try:
            hindi_text = recognizer.recognize_google(audio, language='hi-IN')
            print(f"You said (in Hindi): {hindi_text}")
            return hindi_text
        except Exception:
            print("Sorry, I couldn't understand.")
            return None

# Translate
def translate_to_english(hindi_text):
    translated_text = GoogleTranslator(source='auto', target='en').translate(hindi_text)
    print(f"Translated (to English): {translated_text}")
    return translated_text

# GPT Response
def get_gpt_response(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "Sorry, I'm having trouble thinking right now."

# Speak
def speak_response(text):
    engine.say(text)
    engine.runAndWait()

# Save conversation
def save_conversation(user_text, bot_response):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{RESPONSE_DIR}/conversation_{timestamp}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"You: {user_text}\n")
        file.write(f"Jarvis: {bot_response}\n")

# Main loop
def run_jarvis():
    while True:
        print("\nJarvis is listening... (Say 'stop' to exit)\n")
        hindi_text = listen_in_hindi()

        if hindi_text:
            english_text = translate_to_english(hindi_text)

            if english_text.lower() in ["stop", "exit", "quit"]:
                speak_response("Goodbye!")
                break

            gpt_response = get_gpt_response(english_text)
            print("Jarvis says:", gpt_response)
            speak_response(gpt_response)

            save_conversation(english_text, gpt_response)

# Run
run_jarvis()
