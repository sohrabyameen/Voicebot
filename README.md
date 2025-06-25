# Voicebot
A voicebot to answer your questions.

Aim : To built an Audio Bot which will listen the question and speak the answer.

Approach followed: 
	1. Accepting the speech from device and transcript using speechrecognition.
	2. Make an api call to Gemini using langchain, give question as input and take the answer as response.
	3. Speak the answer using PYTTS text to speech module.

Project Structure:
	1. Config.py : declaration of all the global varables, flags and threads.
	2. Utils.py : set up the LLM and the session state for memory, contains main(): to accept speech and llm call, speak():to speak the answer, stop_speaking(): to stop when button is pressed.
	3. App.py: Define the streamlit app UI

How to execute:
	Make a virtual environment. 1. Install requirements.txt  2. Set the Gemini Api key
	Run 'streamlit run app.py' command in terminal
