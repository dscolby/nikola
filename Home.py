import importlib
import streamlit as st

BODY = """
        This is an experimental tool to transcribe non-English language audio to English 
        language text. The main workhorse behind this functionality is OpenAI's Whisper 
        model, which relies on an encoder/decoder architecture with self attention and cross 
        attention. The interface is designed to be as simple as possible while also allowing
        model settings to be changed.
       """

st.title("English Transcriber")

st.write(BODY)
