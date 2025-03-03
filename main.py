import json
import os
import pyaudio
from vosk import Model, KaldiRecognizer
import openai
import subprocess
import platform

# Configuration & Initialization
openai.api_key = "Please use your API Key"
# Vosk model path (download a model from https://alphacephei.com/vosk/models and unpack it here)
VOSK_MODEL_PATH = "Path to Vosk wherever you have downloaded it to"
if not os.path.exists(VOSK_MODEL_PATH):
    print(f"Please download a Vosk model and unpack it as '{VOSK_MODEL_PATH}' in the current folder.")
    exit(1)

# Initialize Vosk model and recognizer
model = Model(VOSK_MODEL_PATH)
RATE = 16000
CHUNK = 4000  
recognizer = KaldiRecognizer(model, RATE)

# Setup PyAudio for microphone capture
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)
stream.start_stream()


# ChatGPT and TTS Functions (New API Calls)
def chat_with_gpt(transcribed_text):
    conversation = [
        {"role": "developer", "content": "You are a helpful assistant."},
        {"role": "user", "content": transcribed_text}
    ]
    completion = openai.chat.completions.create(
        model="gpt-4o",  
        messages=conversation
    )
    return completion.choices[0].message
    

def text_to_speech(text):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",  
        input=text
    )
    output_filename = "response.mp3"
    response.stream_to_file(output_filename)
    return output_filename

def play_audio(audio_file):
    if os.name == "nt":
        os.system(f"start {audio_file}")
    else:
        if platform.system() == "Darwin":
            os.system(f"afplay {audio_file}")
        else:
            os.system(f"mpg123 {audio_file}")

def handle_chat_response(transcribed_text):
    print("Sending to ChatGPT:", transcribed_text)
    chat_response = chat_with_gpt(transcribed_text)  
    response_text = chat_response.content 
    print("ChatGPT Response:", response_text)
    audio_file = text_to_speech(response_text)  
    play_audio(audio_file)

def process_utterance(text):
    try:
        stream.stop_stream()
    except Exception as e:
        print("Error stopping stream:", e)
    handle_chat_response(text)
    try:
        stream.start_stream()
    except Exception as e:
        print("Error starting stream:", e)

# Main Loop
print("Listening... Speak into your microphone.")

try:
    while True:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
        except Exception as e:
            print("Error reading audio stream:", e)
            break

        if len(data) == 0:
            continue

        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            text = result_dict.get("text", "")
            if text.strip():
                print("Transcription:", text)
                process_utterance(text)
        else:
            pass

except KeyboardInterrupt:
    print("Exiting...")

finally:
    try:
        stream.stop_stream()
        stream.close()
    except Exception:
        pass
    p.terminate()