import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import time

BODY =  """
          The settings below are parameters that will be passed to the OpenAI Whisper model 
          to transcribe the text into English. If you are unsure of what they mean, you can 
          leave them the way they are, as they should work well in most cases. You can also
          experiment with different settings. Be aware that using the large or sometimes 
          medium model might cause the app to crash because is is hosted with Stramlit's 
          free plan. For more information see the OpenAI Whisper 
          [ GitHub page](https://github.com/openai/whisper).
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
                             options=('tiny', 'base', 'small', 'medium', 'large'), 
                             key="whisper_model", index=1)
        temperature = st.number_input("Temperature", 0.00, 1.00, 0.00, step=0.10, 
                                      key="temperature")
        temp_inc = st.number_input("Temperature Increment On Fallback", 0.00, 1.00, 0.20, 
                                   step=0.10, key="temperature_increment_on_fallback")
        no_speech = st.number_input("No Speech Threshold", 0.00, 1.00, 0.60, 
                                    step=0.10, key="no_speech_threshold")
        logprob = st.number_input("Log Probability Threshold", -20.0, 0.0, -1.0, 
                                  step=0.50, key="logprob_threshold")
        compression = st.number_input("Compression Ratio Threshold", 0.0, 10.0, 2.40, 
                                      step=0.20, key="compression_ratio_threshold")
        previous_text = st.checkbox("Condition On Previous Text", 
                                    key="condition_on_previous_text", value=True)
        timestamps = st.checkbox("Timestamps", key="word_timestamps", value=True)
    
        st.form_submit_button("💾 Save Settings", on_click=save_settings, 
                              args=(model, temperature, temp_inc, no_speech, logprob, 
                                    compression, previous_text, timestamps))

        # Show a success message and clear it after five seconds
        success = st.success("Settings Saved!")
        time.sleep(3)
        success.empty()


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
