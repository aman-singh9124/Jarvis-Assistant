import streamlit as st
from gtts import gTTS
import webbrowser
import datetime
import requests
import os
import uuid

# Optional: Your custom music library
try:
    import musicLibrary
except ImportError:
    musicLibrary = {"music": {"song1": "https://example.com"}}

# Speak function using gTTS
def speak(text):
    st.write(f"**Jarvis:** {text}")
    try:
        tts = gTTS(text=text, lang='en')
        filename = f"temp_{uuid.uuid4()}.mp3"
        tts.save(filename)

        # Works only locally
        if os.name == 'nt':  # Windows
            os.system(f"start {filename}")
        else:  # Linux/macOS
            os.system(f"mpg123 {filename}")
    except Exception as e:
        st.error(f"Speech failed: {e}")

# Show current time
def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

# Show current date
def tell_date():
    today = datetime.date.today().strftime("%B %d, %Y")
    speak(f"Today's date is {today}")

# Get latest news
def get_news():
    api_key = "236aa3dc04964442874b296964d7ada3"
    country = "in"
    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"

    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get("articles", [])[:5]

        if not articles:
            speak("Sorry, I couldn't find any news right now.")
            return

        speak("Here are the top news headlines:")
        for i, article in enumerate(articles, 1):
            title = article['title']
            speak(f"Headline {i}: {title}")

    except Exception as e:
        speak("Sorry, I could not fetch the news.")
        st.error(f"News error: {e}")

# Command handler
def processCommand(command):
    command = command.lower()

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")

    elif "open chatgpt" in command:
        speak("Opening ChatGPT")
        webbrowser.open("https://chat.openai.com")

    elif "open whatsapp" in command:
        speak("Opening WhatsApp Web")
        webbrowser.open("https://web.whatsapp.com")

    elif "play" in command:
        song = command.replace("play", "").strip()
        link = musicLibrary.get("music", {}).get(song)
        if link:
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak(f"Sorry, {song} is not in the music library.")

    elif "time" in command:
        tell_time()

    elif "date" in command:
        tell_date()

    elif "news" in command:
        get_news()

    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        st.stop()

    else:
        speak("Sorry, I didn't understand that.")

# Streamlit App
st.title("🧠 Jarvis - Your Virtual Assistant")
command_input = st.text_input("Type your command below:")

if st.button("Execute") and command_input:
    processCommand(command_input)
