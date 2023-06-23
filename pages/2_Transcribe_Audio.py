import streamlit as st
import os
import whisper

BODY =  """
          The settings below are parameters that will be passed to the OpenAI Whisper model 
          to transcribe the text into English. If you are unsure of what they mean, you can 
          leave them the way they are, as they should work well in most cases. You can also
          experiment with different settings. For more information see the OpenAI Whisper
          [GitHub page](https://github.com/openai/whisper).

        """

# Changes the width of the form so there is not a ton of whitespace
CSS = """
        <style>
        section.main > div {max-width:75rem}
        </style>
     """

st.session_state.update(st.session_state)

# Changes the default navicon in the browser tab
st.set_page_config(page_title="Transcription Settings")

st.markdown(CSS, unsafe_allow_html=True)

audio_file = st.file_uploader("Choose one or more audio files")

model = whisper.load_model(st.session_state.whisper_model)

#with open(uploaded_files.name,"wb") as f: 
      #f.write(uploaded_files.name) 

result = model.transcribe(audio_file.name, **st.session_state)

st.text(result["text"])

#st.text(st.session_state.whisper_model)
