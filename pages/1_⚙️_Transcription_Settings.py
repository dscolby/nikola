import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import time

BODY =  """
          The settings below are parameters that will be passed to the OpenAI Whisper model 
          to transcribe the text into English. If you are unsure of what they mean, you can 
          leave them the way they are, as they should work well in most cases. You can also
          experiment with different settings. If you would like more information on what 
          they do you can go to the OpenAI Whisper [GitHub page](https://github.com/openai/whisper).

          WARNING: Using the medium and large models will cause the server to crash because 
          is hosted on Streamlit's free tier. If you want to use the medium or large model 
          you should run it locally by following [these](https://github.com/dscolby/nikola) 
          instructions.
        """

# Changes the width of the form so there is not a ton of whitespace and adds a title to the
# Menu
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


def setup():
    """
    Set up the basic page structure
    """
    # Changes the default navicon in the browser tab
    st.set_page_config(page_title="Transcription Settings")
    st.markdown(CSS, unsafe_allow_html=True)
    st.session_state.disabled = False
    st.title("Transcription Settings")
    st.write(BODY)


def save_settings(model, temperature, temp_inc, no_speech, logprob, compression, 
                  previous_text, timestamps):
    """Callback function to set the session state with settings to be passed to the Whisper 
        model
    """
    st.session_state.whisper_model = model
    st.session_state.temperature = temperature
    st.session_state.temperature_increment_on_fallback = temp_inc
    st.session_state.no_speech_threshold = no_speech
    st.session_state.logprob_threshold = logprob
    st.session_state.compression_ratio_threshold = compression
    st.session_state.condition_on_previous_text = previous_text
    st.session_state.word_timestamps = timestamps


def model_settings():
    """
    Generate the form for model settings
    """
    with st.form("Model Settings"):
        model = st.selectbox(label="Model", 
                             options=('tiny', 'base', 'small', 'medium', 'large'), index=1)
        temperature = st.number_input("Temperature", 0.00, 1.00, 0.00, step=0.10)
        temp_inc = st.number_input("Temperature Increment On Fallback", 0.00, 1.00, 0.20, 
                                   step=0.10)
        no_speech = st.number_input("No Speech Threshold", 0.00, 1.00, 0.60, 
                                    step=0.10)
        logprob = st.number_input("Log Probability Threshold", -20.0, 0.0, -1.0, step=0.50)
        compression = st.number_input("Compression Ratio Threshold", 0.0, 10.0, 2.40, 
                                      step=0.20)
        previous_text = st.checkbox("Condition On Previous Text", value=True)
        timestamps = st.checkbox("Timestamps", value=True)
    
        submit = st.form_submit_button("💾 Save Settings")

        if submit:
            # Show a success message and clear it after five seconds
            success = st.success("Settings Saved!")
            time.sleep(3)
            success.empty()
            save_settings(model, temperature, temp_inc, no_speech, logprob, compression, 
                          previous_text, timestamps)


def next_page():
    """
    Go to the Transcribe Audio page
    """
    if st.button("📝 Go To Transcribe Audio"):
        switch_page("transcribe audio")


if __name__ == '__main__':
    setup()
    model_settings()
    next_page()
