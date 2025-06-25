import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import streamlit as st


st.set_page_config(page_title="🎙️ Voice AI Bot")

from utils import stop_speaking, main

# Running the Streamlit app with a title and instructions
st.title("🎙️ Voice-Interactive AI Assistant")
st.markdown("""
- **Click "Start Speaking"** to begin a conversation with the AI.
- **Click "Stop"** to immediately halt the AI response.
""")


# Listener for the stop button
if st.button("🎤 Start Speaking"):
    stop_flag = False 

    main()

st.button("🛑 Stop", on_click=stop_speaking)
