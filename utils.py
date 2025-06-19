from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import streamlit as st
import pyttsx3
import threading
import speech_recognition as sr

from config import recognizer, stop_flag, status, response_placeholder, speech_thread




llm = ChatGoogleGenerativeAI(
model="gemini-2.0-flash",
temperature=0.7,
google_api_key="" 
)

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="history")


prompt_template = PromptTemplate(
    input_variables=["history", "input"],
    template="""
keep your answer brief.
Conversation history:
{history}
Human: {input}
AI:"""
)

st.session_state.conversation = LLMChain(
llm=llm,
prompt=prompt_template,
memory=st.session_state.memory,
verbose=True
)

def speak(text):
    try:
        local_engine = pyttsx3.init()
        local_engine.setProperty('rate', 170)
        voices = local_engine.getProperty('voices')
        local_engine.setProperty('voice', voices[1].id)

        if not stop_flag:
            local_engine.say(text)
            local_engine.runAndWait()

        local_engine.stop()

    except RuntimeError:
        pass

def stop_speaking():
    
    stop_flag = True
    try:
        local_engine = pyttsx3.init()
        local_engine.stop()
    except RuntimeError:
        pass

def main():



    try:
        with sr.Microphone() as source:
            status.info("Adjusting for noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            status.info("Listening... Speak now.")
            audio = recognizer.listen(source, timeout=7, phrase_time_limit=10)

            user_input = recognizer.recognize_google(audio)

            response  = st.session_state.conversation.run(user_input)

            response_placeholder.markdown(f"**You:** {user_input}\n\n**AI:** {response}")

            status.info("🗣️ Speaking...")

            global speech_thread

            if speech_thread and speech_thread.is_alive():
                stop_speaking()
                speech_thread.join()

            speech_thread = threading.Thread(target=speak, args=(response,))
            speech_thread.start()

            # Wait for speech to finish before updating status
            speech_thread.join()
            status.success("✅ Done")
    
    except sr.WaitTimeoutError:
        status.error("⏳ Timeout. Please speak more quickly.")
    except sr.UnknownValueError:
        status.error("😕 Could not understand what you said.")
    except sr.RequestError:
        status.error("❌ Could not connect to speech service.")
