import pyttsx3
import speech_recognition as sr
import requests
import webbrowser
from datetime import datetime
import time
from word2number import w2n 

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Speak the given text using text-to-speech and print it."""
    print(f"Jarvis: {text}")  
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for the user's voice command with a retry mechanism and extended timeout."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1.5)  
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)  
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            speak("Sorry, I didn't hear anything. Can you speak louder or try again?")
            return listen()  
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that. Can you please speak more clearly?")
            return listen()  
        except sr.RequestError:
            speak("Sorry, there seems to be an issue with my speech service. Please try again later.")
            return ""

def get_weather():
    """Fetch the weather information for a given city."""
    while True:
        speak("Which city's weather would you like to know?")
        city = listen()
        if city:
            api_key = "51c1945f987ecf18ad879e8906d669f5"  
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            
            try:
                response = requests.get(url)
                response.raise_for_status()  
                data = response.json()

            #check if the city is valid
                if data["cod"] == "404":
                    speak(f"Sorry, I couldn't find the weather for {city}. Please try a different city.")
                    continue  
                
                weather_description = data['weather'][0]['description']
                temperature = data['main']['temp']
                speak(f"The current temperature in {city} is {temperature} degrees Celsius with {weather_description}.")
                break  #break when a valid city is identified
            except requests.RequestException:
                speak("Sorry, I couldn't fetch the weather information. Please try again later.")
                break  # Break on connection issues
        else:
            speak("I didn't understand the city name. Can you please repeat it?")

def search_web(query):
    """Open a web browser to search the given query."""
    speak(f"Searching for {query} on the web.")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def set_reminder(reminder, delay):
    """Set a reminder after the specified delay in seconds and announce the delay."""
    speak(f"Setting a reminder for {reminder} {delay} seconds.") 
    time.sleep(delay) 
    speak(f"Reminder {reminder}")

def respond_to_command(command):
    """Respond to various user commands."""
    # Greetings
    if any(greet in command for greet in ['hello', 'hi', 'hey', 'greetings']):
        speak("Hello! How can I assist you today?")
        return True

    # Time-related queries
    if any(time_query in command for time_query in ['time', 'current time', 'what time is it']):
        now = datetime.now().strftime("%H:%M")
        speak(f"The current time is {now}.")
        return True

    # Date-related queries
    if any(date_query in command for date_query in ['date', 'current date', 'what date is it']):
        today = datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}.")
        return True

    # Day of the week queries
    if any(day_query in command for day_query in ['day', 'what day is it', 'day of the week']):
        day = datetime.now().strftime("%A")
        speak(f"Today is {day}.")
        return True

    # Weather queries
    if any(weather_query in command for weather_query in ['weather', 'current weather', 'what is the weather', 'forecast']):
        get_weather()
        return True

    # Web search
    if any(search_query in command for search_query in ['search', 'find', 'look up', 'google']):
        query = command.replace("search", "").replace("find", "").replace("look up", "").replace("google", "").strip()
        search_web(query)
        return True

    # Reminder setting
    if any(reminder_query in command for reminder_query in ['remind me', 'set a reminder', 'remind me to']):
        reminder = command.replace("remind me to", "").replace("set a reminder", "").strip()
        speak("In how many seconds should I remind you?")
        try:
            delay_input = listen()
            delay = w2n.word_to_num(delay_input)  # Use word2number to convert word input to number
            set_reminder(reminder, delay)
        except ValueError:
            speak("Sorry, I need a valid number to set the reminder.")
        return True
    
    return False 

def main():
    """Main function to handle user commands."""
    speak("Hello I am Jarvis, your voice assistant,how may i help you today?")
    while True:
        command = listen()
        if 'stop' in command:
            speak("Goodbye!")
            break  # Exit the program
        
        # Check if the command was recognized
        if not respond_to_command(command):
            speak("Sorry, I didn't understand that. Please say a valid command.")

if __name__ == "__main__":
    main()
