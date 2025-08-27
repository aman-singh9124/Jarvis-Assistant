import streamlit as st
import webbrowser
from gtts import gTTS
import datetime
import requests
import os
import tempfile

# Optional: Replace this with your own library or dict
music_library = {
    "believer": "https://www.youtube.com/watch?v=7wtfhZwyrcc",
    "faded": "https://www.youtube.com/watch?v=60ItHLz5WEA",
}

# Speak using gTTS
def speak(text):
    st.write("Jarvis:", text)
    try:
        tts = gTTS(text)
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio.name)
        st.audio(temp_audio.name, format="audio/mp3")
    except Exception as e:
        st.error(f"🔈 TTS Error: {e}")

# Time
def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

# Date
def tell_date():
    today = datetime.date.today().strftime("%B %d, %Y")
    speak(f"Today's date is {today}")

# News
def get_news():
    api_key = "236aa3dc04964442874b296964d7ada3"
    country = "in"
    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"

    try:
        response = requests.get(url)
        data = response.json()
        articles = data["articles"][:5]

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

# Command processor
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
        song = command.replace("play", "").strip().lower()
        link = music_library.get(song)
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

# Streamlit UI
def main():
    st.title("🧑‍💻 Jarvis Assistant")
    st.write("Type a command below and Jarvis will respond:")

    command = st.text_input("Enter your command:")

    if st.button("Run Command"):
        if command.strip() != "":
            processCommand(command)
        else:
            st.warning("Please enter a command!")

if __name__ == "__main__":
    main()
