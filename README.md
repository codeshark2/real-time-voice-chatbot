# Real-Time Chatbot with Vosk and OpenAI TTS

This project is a prototype for a real-time chatbot that uses:
- **Vosk** for offline speech-to-text (STT)
- **OpenAI Chat API** (e.g. gpt-4o) for generating responses
- **OpenAI TTS API** for converting text to speech

The system continuously listens to your microphone, transcribes your speech, sends the transcription to ChatGPT, and then converts the response into audio which is played back. The code pauses the microphone stream while processing the response to avoid input overflow, then resumes listening for further conversation.

## Features

- **Real-time Speech-to-Text:** Uses Vosk to convert your spoken words into text.
- **ChatGPT Integration:** Sends the transcribed text as conversation turns to the ChatGPT endpoint.
- **Text-to-Speech (TTS):** Converts the generated ChatGPT response into audio.
- **Cross-Platform Audio Playback:** Uses platform-specific commands (e.g. `afplay` on macOS, `mpg123` on Linux, or `start` on Windows) to play the response audio.

## Prerequisites

- **Python 3.12**  
- **PortAudio:**  
  - On macOS, you may need to install PortAudio using Homebrew:
    ```bash
    brew install portaudio
    ```
- **ffmpeg (Optional):**  
  If you decide to experiment with streaming TTS playback (not used in the final code), install [ffmpeg](https://ffmpeg.org/download.html).

## Setup Instructions

1. **Clone the Repository or Download the Code:**

   Place the provided `main.py`, `requirements.txt`, and `README.md` in a folder.

2. **Download a Vosk Model:**

   - Visit [Vosk Models](https://alphacephei.com/vosk/models) and download an appropriate model (for example, an English model).
   - Unzip the model and place the folder in your project directory.
   - Update the `VOSK_MODEL_PATH` variable in `main.py` with the path to your downloaded model.

3. **Install Dependencies:**

   Create a virtual environment (optional but recommended), then run:
   ```bash
   pip install -r requirements.txt
