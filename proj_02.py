import tkinter as tk
import os
import boto3
import pywhatkit
import random
from tkinter import simpledialog
import speech_recognition as sr
import datetime as dt
import cv2
import time
import requests
import subprocess
import threading
import webbrowser
from googletrans import Translator
import pytz
#from googlecalendarapi import GoogleCalendar

# Initialize the Google Calendar API
#calendar = GoogleCalendar()
# from instabot import Bot  # Commented out to avoid an error, make sure to import it if needed.

myec2 = boto3.client("ec2")
voice_assistance_button = None

def create_basic_window():
    global voice_assistance_button
    root = tk.Tk()
    root.title("Voice-Controlled Assistant")
    root.geometry("400x650")
    
    label = tk.Label(root, text="Voice-Controlled Assistant", font=("Helvetica", 16, "bold"))
    label.pack(pady=10)

    date = dt.datetime.now()
    date_label = tk.Label(root, text="Date: %s" % date.strftime("%Y-%m-%d %H:%M:%S"))
    date_label.pack()

    voice_assistance_button = tk.Button(root, text="Voice Assistance", command=enable_voice_assistance)
    voice_assistance_button.pack(pady=20)

    options = [
        ("Email", on_button_email),
        ("EC2", on_button_ec2),
        ("Add S3 Bucket", s3_bucket_create),
        ("Notepad", on_button_click),
        ("Chrome", on_click),
        ("Paint", on_click_paint),
        ("Word", on_click_word),
        ("Play on YouTube", youtube_music),
        ("Take Photo", take_photo),
    ]

    for option_text, command in options:
        button = tk.Button(root, text=option_text, command=command)
        button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", width=10, fg="#fff", bg="#f00", command=root.destroy)
    exit_button.pack(pady=10)

    root.mainloop()

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        user_input = recognizer.recognize_google(audio)
        print(f"User said: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return None
    except sr.RequestError:
        print("There was a problem with the speech recognition service.")
        return None

def enable_voice_assistance():
    global voice_assistance_button

    voice_assistance_button.config(state=tk.DISABLED)
    user_input = get_voice_input()
    if user_input:
        process_voice_command(user_input)
    voice_assistance_button.config(state=tk.ACTIVE)


def process_voice_command(command):

    if "email" in command:
        on_button_email()
    elif "EC2" in command:
        on_button_ec2()
    elif "notepad" in command:
        on_button_click()
    elif "chrome" in command:
        on_click()
    elif "paint" in command:
        on_click_paint()
    elif "word" in command:
        on_click_word()
    elif "weather" in command:
        city = command.split("weather in ")[-1]
        result = get_weather(city)
        print(result)
    elif "news" in command:
        category = command.split("news ")[-1]
        news = get_news_headlines(category)
        print(news)
    elif "calculate" in command:
        expression = command.split("calculate ")[-1]
        result = calculate(expression)
        print(result)
    elif "reminder" in command:
        parts = command.split("reminder ")[-1].split(" at ")
        time = parts[1]
        message = parts[0]
        set_reminder(time, message)
    elif "translate" in command:
        parts = command.split("translate ")[-1].split(" to ")
        text = parts[0]
        target_language = parts[1]
        result = translate_text(text, target_language)
        print(result)
    elif "search" in command:
        query = command.split("search for ")[-1]
        result = search_web(query)
        print(result)
    
        print(result)
    elif "play music" in command:
        song = command.split("play music ")[-1]
        result = play_music(song)
        print(result)
    elif "fun fact" in command:
        fact = get_fun_fact()
        print(fact)
    elif "send message" in command:
        parts = command.split("send message ")[-1].split(" to ")
        phone_number = parts[1]
        message = parts[0]
        result = send_text_message(phone_number, message)
        print(result)
    
    elif "system operation" in command:
        operation = command.split("system operation ")[-1]
        result = perform_system_operation(operation)
        print(result)
    elif "send message" in command:
        parts = command.split("send message ")[-1].split(" to ")
        phone_number = parts[1]
        message = parts[0]
        result = send_text_message(phone_number, message)
        print(result)
    
    elif "system operation" in command:
        operation = command.split("system operation ")[-1]
        result = perform_system_operation(operation)
        print(result)
    else:
        print("Command not recognized.")

def on_button_ec2():
    response = myec2.run_instances(
        ImageId='ami-0ded8326293d3201b',
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1
    )
    print("EC2 instance started.")

def on_button_email():
    msg = "Hello from python"
    recipient_email = get_voice_input()
    if not recipient_email:  # If voice input fails, use text-based input dialog
        recipient_email = simpledialog.askstring("Input", "Enter recipient's email address:")
    if recipient_email:
        pywhatkit.send_mail("testprect@gmail.com", "aljeobaueiacqtko", "test code", msg, recipient_email)
        print("Email sent.")

def on_button_click():
    os.system("notepad")

def on_click():
    os.system("start chrome")
    
def on_click_paint():
    os.system("start mspaint")

def on_click_word():
    os.system("start winword")
    
def s3_bucket_create():
    ec2_client = boto3.client('ec2')
    response_ec2 = ec2_client.describe_instances()

    # Create an S3 Instance
    s3_client = boto3.client('s3')

    # Call create_bucket to create an S3 bucket
    response_s3 = s3_client.create_bucket(
        ACL='private',  # Use 'private' instead of 'enabled' for private ACL
        Bucket='shajafi',
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-south-1'  # Use the region code, not the region name
        }
    )
    print("S3 bucket created.")
def send_text_message(phone_number, message):
    try:
        # Use an SMS API here to send the message to the specified phone number
        # Example: sms_api.send_message(phone_number, message)
        return f"Message sent to {phone_number}: '{message}'"
    except Exception as e:
        return f"Error sending text message: {e}"

# Function to set a timer
""" def set_timer(minutes):
    try:
        seconds = int(minutes) * 60
        threading.Timer(seconds, timer_expired).start()
        return f"Timer set for {minutes} minutes."
    except Exception as e:
        return f"Error setting timer: {e}" """
def perform_system_operation(operation):
    try:
        if operation == "shutdown":
            subprocess.run(["shutdown", "/s", "/t", "1"])
            return "Shutting down the system."
        elif operation == "restart":
            subprocess.run(["shutdown", "/r", "/t", "1"])
            return "Restarting the system."
        else:
            return "Invalid system operation."
    except Exception as e:
        return f"Error performing system operation: {e}"

def youtube_music():
    
    final_music = "dil meri na sune"
    print(f"playing {final_music} on youtube")
    pywhatkit.playonyt(final_music)

def take_photo():
    cap = cv2.VideoCapture(0)
    time.sleep(1)
    ret, frame = cap.read()
    if ret:
        cv2.imshow('photo.jpg', frame)
        cv2.imwrite('photo.jpg',frame)
        cap.release()
        cv2.destroyAllWindows()
        print("Photo captured.")
def get_weather(city):
    # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    api_key = 'YOUR_API_KEY'
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    response = requests.get(base_url)
    data = response.json()

    if data["cod"] != "404":
        weather_data = data["weather"][0]["description"]
        temperature = data["main"]["temp"]

        return f"The weather in {city} is {weather_data}. The temperature is {temperature}°C."
    else:
        return "City not found."
def get_news_headlines(category="general"):
    # Replace 'YOUR_NEWS_API_KEY' with your actual news API key
    news_api_key = 'YOUR_NEWS_API_KEY'
    base_url = f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={news_api_key}'

    response = requests.get(base_url)
    data = response.json()

    if data["status"] == "ok" and data["totalResults"] > 0:
        headlines = [article["title"] for article in data["articles"]]
        return "\n".join(headlines)
    else:
        return "No news articles found."
def calculate(expression):
    try:
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error: {e}"

# Function to set reminders and alarms
def set_reminder(time, message):
    try:
        alarm_time = dt.datetime.strptime(time, "%H:%M")
        current_time = dt.datetime.now()
        if alarm_time < current_time:
            alarm_time = alarm_time + dt.timedelta(days=1)

        delta = alarm_time - current_time
        seconds = delta.seconds
        time.sleep(seconds)
        print(f"Reminder: {message}")
    except Exception as e:
        print(f"Error setting reminder: {e}")
def translate_text(text, target_language):
    try:
        translated_text = Translator.translate(text, dest=target_language)
        return f"Translated to {target_language}: {translated_text.text}"
    except Exception as e:
        return f"Translation error: {e}"

# Function for web search
def search_web(query):
    try:
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        return f"Searching the web for {query}."
    except Exception as e:
        return f"Web search error: {e}"
# Function to add an event to the calendar


# Music playlist
music_playlist = {
    "song1": "https://www.youtube.com/watch?v=VIDEO_ID",
    "song2": "https://www.youtube.com/watch?v=VIDEO_ID",
    "song3": "https://www.youtube.com/watch?v=VIDEO_ID",
}
# Function to play music
def play_music(song):
    try:
        if song in music_playlist:
            webbrowser.open(music_playlist[song])
            return f"Now playing {song}."
        else:
            return f"Song not found in the playlist."
    except Exception as e:
        return f"Error playing music: {e}"

# Fun facts
fun_facts = [
    "Did you know that honey never spoils?",
    "Bananas are berries, but strawberries aren't.",
    "Octopuses have three hearts.",
]
def get_fun_fact():
    return random.choice(fun_facts)
create_basic_window()
