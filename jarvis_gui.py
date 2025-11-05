import streamlit as st
import streamlit.components.v1 as components
import speech_recognition as sr
import pyttsx3
import datetime
import requests
import musicLibrary 
import traceback
try:
    engine = pyttsx3.init('sapi5')  
except Exception:
    try:
        engine = pyttsx3.init()  
    except Exception:
        engine = None

if engine:
    engine.setProperty('rate', 180)
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)

recognizer = sr.Recognizer()

def speak(text):
    """Speak and also show in UI."""
    st.session_state["response"] = text
   
    try:
        if engine:
            engine.say(text)
            engine.runAndWait()
    except Exception:
       
        traceback.print_exc()

def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

def tell_date():
    today = datetime.date.today().strftime("%B %d, %Y")
    speak(f"Today's date is {today}")

def get_news():
    api_key = "236aa3dc04964442874b296964d7ada3"  # your key
    country = "in"
    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"
    try:
        response = requests.get(url, timeout=7)
        data = response.json()
        articles = data.get("articles", [])[:5]
        if not articles:
            speak("Sorry, I couldn't find any news right now.")
            return
        speak("Here are the top news headlines:")
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'No title')
            st.write(f"📰 {title}")
            if engine:
                engine.say(f"Headline {i}: {title}")
        if engine:
            engine.runAndWait()
    except Exception as e:
        st.error("Couldn't fetch news.")
        speak("Sorry, I could not fetch the news.")

def open_website(url):
    """
    Uses Streamlit components HTML to run client-side JS that opens a new tab.
    This is what makes the browser open YouTube automatically.
    """
    
    js = f"""
    <script>
      try {{
        window.open("{url}", "_blank");
      }} catch (e) {{
        console.log("Couldn't open window:", e);
      }}
    </script>
    """
    components.html(js, height=0, width=0)

def processCommand(command):
    command = command.lower()
    try:
        if "open google" in command:
            speak("Opening Google")
            open_website("https://google.com")

        elif "open youtube" in command:
            speak("Opening YouTube")
            open_website("https://youtube.com")

        elif "open facebook" in command:
            speak("Opening Facebook")
            open_website("https://facebook.com")

        elif "open linkedin" in command:
            speak("Opening LinkedIn")
            open_website("https://linkedin.com")

        elif "open chatgpt" in command:
            speak("Opening ChatGPT")
            open_website("https://chat.openai.com")

        elif "open whatsapp" in command or "whatsapp" in command:
            speak("Opening WhatsApp Web")
            open_website("https://web.whatsapp.com")

        elif "time" in command:
            tell_time()

        elif "date" in command:
            tell_date()

        elif "news" in command:
            get_news()

        elif "play" in command:
           
            song = command.replace("play", "").strip().lower()
            link = musicLibrary.music.get(song)
            if link:
                speak(f"Playing {song}")
                open_website(link)
            else:
                speak(f"Sorry, {song} is not in the music library. I will show a link.")
                st.write(f"No such song in library. Try searching: [Search {song} on YouTube](https://www.youtube.com/results?search_query={song.replace(' ', '+')})")

        else:
            speak("Sorry, I didn't understand that.")
    except Exception as e:
        st.error("Error when processing command.")
        traceback.print_exc()
        speak("Sorry, something went wrong while processing the command.")


st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background-color: #000000; color: #00ffff; }
    .robot-face { text-align: center; margin-top: 20px; }
    .eye {
        width: 50px; height: 50px;
        background: radial-gradient(circle, #00ffff 30%, #000 90%);
        border-radius: 50%; display: inline-block;
        margin: 0 20px; animation: blink 5s infinite;
    }
    @keyframes blink {
        0%, 90%, 100% { height: 50px; }
        95% { height: 10px; }
    }
    .mouth {
        width: 150px; height: 10px;
        background: linear-gradient(to right, #00ffff, #00ffcc);
        margin: 25px auto; border-radius: 5px;
        animation: speak 1s infinite alternate;
    }
    @keyframes speak {
        0% { transform: scaleY(1); }
        100% { transform: scaleY(3); }
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center; color:#00ffff;'>🤖 Jarvis Assistant</h1>", unsafe_allow_html=True)

st.markdown("""
<div class='robot-face'>
    <div class='eye'></div>
    <div class='eye'></div>
    <div class='mouth'></div>
</div>
""", unsafe_allow_html=True)

if "response" not in st.session_state:
    st.session_state["response"] = "Say 'Jarvis' to activate me!"

st.write("🎤 Click the button below and speak your command (examples: 'open YouTube', 'open LinkedIn', 'shape of you'):")


def microphone_callback():
    """
    Listens on the server/local machine mic using speech_recognition and runs processCommand.
    Note: This will use your machine's microphone (not browser mic).
    """
    with st.spinner("Listening..."):
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=6)
                command = recognizer.recognize_google(audio)
                st.success(f"You said: {command}")
                processCommand(command)
        except sr.UnknownValueError:
            st.error("Sorry, I didn’t catch that. Try again.")
            speak("Sorry, I didn't catch that. Please try again.")
        except sr.RequestError as e:
            st.error("Speech recognition service error. Check internet.")
            speak("Speech recognition service error.")
        except Exception as e:
            st.error(f"Error: {e}")
            traceback.print_exc()
            speak("An error occurred while listening.")


st.button("🎙️ Activate Jarvis", on_click=microphone_callback)


st.markdown(
    f"<h3 style='text-align:center; color:#00ffff;'>{st.session_state['response']}</h3>",
    unsafe_allow_html=True,
)

st.caption("Created in Python by Aman Singh")
