import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from datetime import date
import os
import whisper
from streamlit.web.server.server import TORNADO_SETTINGS

# Change ping timeout so that long running transcriptions do not time out
TORNADO_SETTINGS["websocket_ping_timeout"] = 600

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


@st.cache(show_spinner=False, ttl=1)
def transcribe_recording(re):
    """
    Transcribe uploaded text with OpenAI Whisper

    Parameters:
        (str) re: the path to an audio file
    """
    model = whisper.load_model(st.session_state.whisper_model)
    result = model.transcribe(re, task="translate", beam_size=5, best_of=5, fp16=False)
    segments = result["segments"]

    with open("temp/output.txt", "w") as f:
        for segment in segments:
            if st.session_state.word_timestamps:
                l = str(segment["start"]) + segment["text"] + "\n"
            else:
                l = segment["text"] + "\n"

            f.write(l)


def transcribe_with_spinner():
    """
    Transcribes an audio file and manages the spinner
    """
    # Load an audio file and model
    audio_file = st.file_uploader("Choose a file to transcribe", 
                              type=["mp4", "avi", "mov", "mkv", "mp3", "wav", "m4a", "ogg"])
    
    # Write the uploaded file to a temporary folder and transcribe that file
    if audio_file:
        filepath = os.path.join("temp", audio_file.name)
        with open(filepath,"wb") as f:
            f.write(audio_file.getbuffer())

        with st.spinner("Transcription in progress"):
            transcribe_recording(filepath)
        del audio_file


def download_file():
    """
    Downloads a transcript to the user's computer
    """
    if os.path.isfile("temp/output.txt"):
        text_file = open("temp/output.txt")
        today = date.today()
        if st.download_button("Download Transcript", text_file, 
                              file_name="transcribed_audio_" + str(today) + ".txt"):
            switch_page("about")


if __name__ == '__main__':
    # If there are no model settings saved, use the defaults
    # This happens if a user goes from About to Transcribe Audio and before saving settings
    if not st.session_state:
        set_defaults()

    transcribe_with_spinner()
    download_file()

