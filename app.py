import streamlit as st
import datetime
import wikipedia
import urllib.parse
from gtts import gTTS
from io import BytesIO

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="AI Virtual Assistant",
    page_icon="🤖",
    layout="centered"
)

# ================== TEXT TO SPEECH ==================
def talk(text):
    tts = gTTS(text=text, lang="en")
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    st.audio(audio_bytes.getvalue(), format="audio/mp3")

# ================== ASSISTANT LOGIC ==================
def run_assistant(command):

    # PLAY SONG ON YOUTUBE
    if command.startswith("play"):
        song = command.replace("play", "").strip()
        query = urllib.parse.quote(song)
        url = f"https://www.youtube.com/results?search_query={query}"
        response = f"Playing {song} on YouTube."
        talk(response)
        st.link_button("▶ Play on YouTube", url)
        return response

    # CURRENT TIME
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The current time is {current_time}."
        talk(response)
        return response

    # WIKIPEDIA SEARCH
    elif command.startswith("search"):
        topic = command.replace("search", "").strip()
        try:
            info = wikipedia.summary(topic, sentences=2)
            talk(info)
            return info
        except wikipedia.exceptions.DisambiguationError:
            response = "Please be more specific in your search."
            talk(response)
            return response
        except wikipedia.exceptions.PageError:
            response = "Sorry, I could not find information on that topic."
            talk(response)
            return response

    # OPEN YOUTUBE
    elif "open youtube" in command:
        url = "https://www.youtube.com"
        response = "Opening YouTube."
        talk(response)
        st.link_button("📺 Open YouTube", url)
        return response

    # WHO ARE YOU
    elif "who are you" in command:
        response = "I am a browser based AI virtual assistant created using Python and Streamlit."
        talk(response)
        return response

    # GREETING
    elif "hello" in command or "hi" in command:
        response = "Hello! How can I assist you today?"
        talk(response)
        return response

    # DEFAULT
    else:
        response = "Sorry, I do not understand that command yet."
        talk(response)
        return response


# ================== UI ==================
st.title("🤖 AI Browser-Based Virtual Assistant")
st.write("Interact with your assistant below 👇")

# Greeting on Start
if "first_load" not in st.session_state:
    st.session_state.first_load = True
    welcome_message = "Hello, welcome to your AI Virtual Assistant. How can I help you today?"
    talk(welcome_message)
    st.info(welcome_message)

# ================== USER INPUT ==================
command = st.text_input(
    "💬 Enter your command",
    placeholder="Example: play nasheed, search AI, what is the time"
)

if st.button("🚀 Run Assistant"):
    if command.strip():
        st.success(f"You said: {command}")
        reply = run_assistant(command.lower())
        st.info(reply)
    else:
        st.warning("Please enter a command.")

# ================== SUGGESTED QUESTIONS ==================
st.subheader("💡 Try These Commands")

suggested_questions = [
    "hello",
    "play how to create chatbot",
    "search artificial intelligence",
    "what is the time",
    "open youtube",
    "who are you"
]

for question in suggested_questions:
    if st.button(question):
        st.success(f"You said: {question}")
        reply = run_assistant(question.lower())
        st.info(reply)