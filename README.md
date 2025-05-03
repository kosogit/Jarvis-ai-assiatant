# Jarvis-ai-assiatant
Jarvis is a voice-controlled personal assistant built using Python, OpenAI's GPT-3, and several popular libraries such as SpeechRecognition, pyttsx3, and DeepTranslator. I made this in my 12 grade.  It allows you to interact with your computer using natural speech, with the capability to translate Hindi to English, get GPT-3 responses, and save conversations to text files.
Features:
Speech Recognition: Listen to commands in Hindi using the SpeechRecognition library.

Text-to-Speech: Get spoken responses using the pyttsx3 engine.

Google Translator: Translates Hindi speech into English.

OpenAI GPT-3 Integration: Generates intelligent, human-like responses via GPT-3.

Conversation Logging: Saves interactions in a folder for later review.

How It Works:
Voice Command: Jarvis listens for Hindi speech commands.

Translation: The speech is translated to English using Google Translator.

Processing: The translated text is sent to OpenAI's GPT-3 to generate a response.

Response: Jarvis speaks the generated response aloud and saves the conversation for future reference.

Installation:
Clone the repository:


git clone https://github.com/kosogit/jarvis-ai-assistant.git

Navigate to the project folder:

"cd jarvis-ai-assistant"

Install the required dependencies:


"pip install -r requirements.txt"
Set your OpenAI API key in the script where indicated (openai.api_key = "your_openai_api_key").

Requirements:
Python 3.6+

OpenAI API Key

Required Libraries:

speech_recognition

pyttsx3

deep-translator

openai

os

datetime

Usage:
Run the main Python script:

there are two file select 1st one dont use chat gpi api it use responce folder to give reply you can use any file insted of reponce.txt to get responce 
and 2.py use openai to give responce .

"python 1.py"
"python 2.py" 

Speak your command in Hindi. Jarvis will process it, respond, and save the conversation in the responses folder.

Example Commands:
"Hello Jarvis" – Jarvis will greet you.

"What is the weather?" – Jarvis will fetch weather information (if integrated).

"Tell me a joke" – Jarvis will tell you a random joke.

"Stop" – To end the interaction.

Contributing:
Feel free to fork this project, contribute to the codebase, or suggest improvements via pull requests. Contributions are welcome!

License:
This project is licensed under the MIT License - see the LICENSE file for details.
