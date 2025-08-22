import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import datetime
import requests

# Initialize TTS engine
engine = pyttsx3.init('sapi5')  # use 'espeak' if on Linux
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

recognizer = sr.Recognizer()

# Speak function
def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

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
            print(f"{i}. {title}")

    except Exception as e:
        speak("Sorry, I could not fetch the news.")
        print("News error:", e)

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
        song = command.replace("play", "").strip()
        link = musicLibrary.music.get(song)
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
        exit()

    else:
        speak("Sorry, I didn't understand that.")

# Main program loop
if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("\nSay 'Jarvis' to activate...")
                audio = recognizer.listen(source, timeout=4, phrase_time_limit=2)
                try:
                    wake_word = recognizer.recognize_google(audio)
                    print("Heard:", wake_word)
                    if wake_word.lower() == "jarvis":
                        print("Jarvis activated...")
                        speak("Yes, how can I help you?")

                        # Listen for actual command
                        with sr.Microphone() as source2:
                            recognizer.adjust_for_ambient_noise(source2, duration=0.5)
                            print("Listening for your command...")
                            audio2 = recognizer.listen(source2, timeout=4, phrase_time_limit=5)
                            command = recognizer.recognize_google(audio2)
                            print("Command received:", command)
                            processCommand(command)

                except sr.UnknownValueError:
                    print("Could not recognize the wake word.")
        except Exception as e:
            print("Error:", e)