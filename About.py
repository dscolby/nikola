import streamlit as st
import os
from streamlit_extras.switch_page_button import switch_page

BODY = """
        Nikola is an experimental tool to transcribe non-English language audio to English 
        language text. The main workhorse behind this functionality is OpenAI's Whisper 
        model, which relies on an encoder/decoder architecture with self attention and cross 
        attention. The interface is designed to be as simple as possible while also allowing
        model settings to be changed. The original purpose of Nikola was to enable 
        transcribing recorded interviews with former members of the FARC and civilians 
        affected by the Colombian Conflict from Spanish audio to English text. However, 
        Nikola can transcribe many other languages. 
        [Here](https://help.openai.com/en/articles/7031512-whisper-api-faq) is a list of 
        supported languages.
       """

for file in os.listdir("temp"):
    os.remove(f"temp/{file}")

# Changes the default navicon in the browser tab
st.set_page_config(page_title="About")

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
