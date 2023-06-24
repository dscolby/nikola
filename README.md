# Nikola

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

## Using Nikola
An online version of Nikola is available [here](https://nikola.streamlit.app).

Using Nikola locally requires installing ffmpeg as follows.

```
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

Then, clone the repo and change the working directory like so.

```
git clone https://github.com/dscolby/nikola.git
cd nikola
```

Use pip to set up a virtual environment and install the requirements shown below.

```
# Unix/macOS
python3 -m venv env
source env/bin/activate

# Windows
py -m venv env
.\env\Scripts\activate

pip install -r requirements.txt
```

Finally, run the app.

```
streamlit run About.py
```