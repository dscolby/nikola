import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from datetime import date
import os
import whisper

BODY =  """
          The settings below are parameters that will be passed to the OpenAI Whisper model 
          to transcribe the text into English. If you are unsure of what they mean, you can 
          leave them the way they are, as they should work well in most cases. You can also
          experiment with different settings. For more information see the OpenAI Whisper
          [GitHub page](https://github.com/openai/whisper).

        """

# Changes the width of the form so there is not a ton of whitespace and adds a title to the
# menu bar
CSS = """
        <style>
        section.main > div {max-width:75rem}
        </style>

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
     """

st.session_state.update(st.session_state)

# Changes the default navicon in the browser tab
st.set_page_config(page_title="Transcription Settings")

st.markdown(CSS, unsafe_allow_html=True)


def set_defaults():
    """
    Set the session state with defaults for the OpenAI Whisper base model
    """
    # Set session state variables to OpenAI Whisper defaults in case the user does not set them
    st.session_state.whisper_model = 'base'
    st.session_state.temperature = 0.00
    st.session_state.temperature_increment_on_fallback = 0.20
    st.session_state.no_speech_threshold = 0.6
    st.session_state.logprob_threshold = -1.0
    st.session_state.compression_ratio_threshold = 2.40
    st.session_state.condition_on_previous_text = True
    st.session_state.word_timestamps = True
    st.session_state.verbose = False


@st.cache
def transcribe_recording(re):
    """
    Transcribe uploaded text with OpenAI Whisper

    Parameters:
        (str) re: the path to an audio file
    """
    model = whisper.load_model("base")
    result = model.transcribe(re, task="translate", beam_size=5, best_of=5, fp16=False)
    segments = result["segments"]

    with open("temp/output.txt", "w") as f:
        for segment in segments:
            if st.session_state.word_timestamps:
                l = str(segment["start"]) + segment["text"] + "\n"
            else:
                l = segment["text"] + "\n"

            f.write(l)


# If there are no model settings saved, use the defaults
# This can happen if a user goes from Aout to Transcribe Audio and does not save settings
if not st.session_state or len(st.session_state) != 9:
    set_defaults()

# Load an audio file and model
audio_file = st.file_uploader("Choose a file to transcribe", 
                              type=["mp4", "avi", "mov", "mkv", "mp3", "wav", "m4a", "ogg"])
model = whisper.load_model(st.session_state.whisper_model)

# Write the uploaded file to a temporary folder and transcribe that file
if audio_file:
    filepath = os.path.join("temp", audio_file.name)
    with open(filepath,"wb") as f:
        f.write(audio_file.getbuffer())

    with st.spinner("Transcription in progress"):
        transcribe_recording(filepath)
    del audio_file
        

if os.path.isfile("temp/output.txt"):
    text_file = open("temp/output.txt")
    today = date.today()
    if st.download_button("Download Transcript", text_file, 
                          file_name="transcribed_audio_" + str(today) + ".txt"):
        switch_page("about")
