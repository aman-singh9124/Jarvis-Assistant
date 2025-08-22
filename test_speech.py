import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # or voices[1].id for female

print("Speaking...")
engine.say("Yes, I am speaking. Can you hear me?")
engine.runAndWait()
print("Done")
