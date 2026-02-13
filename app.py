import streamlit as st
from translate import Translator
import requests
import os

# --- APP CONFIG ---
st.set_page_config(page_title="ElevenLabs Translator App", page_icon="🎙️")
st.title("🎙️ AI Voice Translator")

# --- 1. GET API KEY FROM FILE ---
# We check if the file exists first so the app doesn't crash
if os.path.exists("EL API.txt"):
    with open("EL API.txt", "r") as f:
        API_KEY = f.read().strip()
else:
    st.error("🔑 API Key File Missing! Please create 'EL API.txt' in this folder.")
    st.stop()

VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

# --- 2. SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("Settings")
    target_lang = st.selectbox("Target Language", ["Original (No Translation)", "es", "fr", "de", "it", "ja", "ko"])
    model = st.selectbox("Model", ["eleven_multilingual_v2", "eleven_flash_v2_5"])

# --- 3. MAIN INTERFACE ---
text_input = st.text_area("Paste your text here or upload a file below:", height=200)
uploaded_file = st.file_uploader("Choose a .txt file", type="txt")

if uploaded_file:
    text_input = uploaded_file.read().decode("utf-8")

if st.button("Generate Audio"):
    if not text_input:
        st.error("Please provide some text!")
    else:
        # Step A: Translation Logic
        final_text = text_input
        if target_lang != "Original (No Translation)":
            st.info(f"Translating to {target_lang}...")
            try:
                translator = Translator(to_lang=target_lang)
                # Clean up the "Translated by..." watermark if it appears
                final_text = translator.translate(text_input).split("Translated by")[0]
            except Exception as e:
                st.error(f"Translation failed: {e}")
                st.stop()

        # Step B: ElevenLabs API Request
        st.info("Generating audio...")
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
        data = {"text": final_text, "model_id": model}

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            st.success("Success!")
            st.audio(response.content, format="audio/mp3")
            st.download_button("Download MP3", response.content, file_name="output.mp3")
        else:
            st.error(f"ElevenLabs Error: {response.text}")