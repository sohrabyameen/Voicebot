import speech_recognition as sr
import threading
import streamlit as st 



speech_thread = None
stop_flag = False
lock = threading.Lock()
recognizer = sr.Recognizer()
status = st.empty() 
response_placeholder = st.empty()