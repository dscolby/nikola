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


def transcribe_recording(re):
    """
    Transcribe uploaded text with OpenAI Whisper

    Parameters:
        (str) re: the path to an audio file
    """
    model = whisper.load_model("base")
    result = model.transcribe(re, task="translate", beam_size=3, best_of=3, fp16=False)
    segments = result["segments"]

    with open("temp/output.txt", "w") as f:
        for segment in segments:
            l = str(segment["start"]) + segment["text"] + "\n"
            f.write(l)


# Load an audio file and model
audio_file = st.file_uploader("Choose one or more audio files")
model = whisper.load_model(st.session_state.whisper_model)

# Write the uploaded file to a temporary folder and transcribe that file
if audio_file:
    filepath = os.path.join("temp", audio_file.name)
    with open(filepath,"wb") as f:
         f.write(audio_file.getbuffer())
    transcribe_recording(filepath)
