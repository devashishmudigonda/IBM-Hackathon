# record_stream.py
import sounddevice as sd
import numpy as np
import queue
import tempfile
import whisper
import time
import requests

AUDIO_RATE = 16000
BLOCK_DURATION = 5  # seconds
QUEUE = queue.Queue()

def audio_callback(indata, frames, time_info, status):
    if status:
        print(f"[!] Audio stream warning: {status}")
    QUEUE.put(indata.copy())

def transcribe_and_summarize(audio_data):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        write_audio = (audio_data * 32767).astype(np.int16)
        import scipy.io.wavfile
        scipy.io.wavfile.write(f.name, AUDIO_RATE, write_audio)

        model = whisper.load_model("base")
        result = model.transcribe(f.name)
        transcript = result["text"]

        print("🗣️ Transcript:", transcript)

        # Send to Flask API for summary
        resp = requests.post("http://127.0.0.1:5000/summarize", json={"transcript": transcript})
        print("📝 Summary:\n", resp.json().get("output"))

def start_recording():
    print("🎤 Listening to system audio via BlackHole (press Ctrl+C to stop)...")

    with sd.InputStream(channels=1, callback=audio_callback, samplerate=AUDIO_RATE, blocksize=int(AUDIO_RATE * BLOCK_DURATION)):
        while True:
            frames = []
            for _ in range(0, int(60 / BLOCK_DURATION)):  # Summarize every ~60 seconds
                data = QUEUE.get()
                frames.append(data)
            audio_data = np.concatenate(frames, axis=0)
            transcribe_and_summarize(audio_data)

if __name__ == "__main__":
    start_recording()
