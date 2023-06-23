import streamlit as st
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
    segments_list = []
    model = whisper.load_model("base")
    result = model.transcribe(re.name, task="translate", beam_size=3, best_of=3, fp16=False)
    text_file = open("download/output.txt", "w")
    segments = result["segments"]

    for segment in segments:
        segments_list.append(str(segment["start"]) + segment["text"] + "\n")
        text_file.write("{}".format(segment + "\n"))


# Load an audio file and model
audio_file = st.file_uploader("Choose one or more audio files")
model = whisper.load_model(st.session_state.whisper_model)

if audio_file:
    transcribe_recording(audio_file)
