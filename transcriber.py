# transcriber.py
import sounddevice as sd
import numpy as np
import whisper
import threading
import time

class LiveTranscriber:
    def __init__(self):
        self.model = whisper.load_model("base")
        self.transcript = ""
        self.recording = False
        self.interval = 10  # seconds per recording chunk

    def start_transcription(self):
        self.recording = True
        threading.Thread(target=self._record_loop).start()

    def _record_loop(self):
        while self.recording:
            audio = sd.rec(int(self.interval * 16000), samplerate=16000, channels=1, dtype='float32')
            sd.wait()
            audio_np = np.squeeze(audio)

            # Save temporary file
            whisper.audio.save_audio(audio_np, "temp.wav", 16000)
            result = self.model.transcribe("temp.wav", fp16=False)
            self.transcript += " " + result['text']

    def get_transcript(self):
        return self.transcript.strip()

    def stop(self):
        self.recording = False
