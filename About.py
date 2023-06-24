import streamlit as st
import os
from streamlit_extras.switch_page_button import switch_page

BODY = """
        Nikola is an experimental tool to transcribe non-English language audio to English 
        language text. The main workhorse behind this functionality is OpenAI's Whisper 
        model, which relies on an encoder/decoder architecture with self attention and cross 
        attention. The interface is designed to be as simple as possible while also allowing
        model settings to be changed.
       """

for file in os.listdir("temp"):
    os.remove(f"temp/{file}")

st.title("Nikola")

st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "Menu";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
)



st.write(BODY)

if st.button("📝 Go To Transcription Settings"):
    switch_page("transcription settings")
