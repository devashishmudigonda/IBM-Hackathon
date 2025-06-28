from flask import Flask, request, jsonify, render_template
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames
import whisper, tempfile, subprocess, threading, time, os

app = Flask(__name__)

# IBM Watson Credentials
credentials = Credentials.from_dict({
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": "eUtvlc1m_NxqEJGX5nof07Y-TIISdJBKyUrEwK1vkYTd"
})
inference = ModelInference(
    model_id="ibm/granite-3-2b-instruct",
    project_id="6f6af590-901e-4508-ae02-8a3ecf7498d1",
    credentials=credentials
)
model = whisper.load_model("base")

live_running = False
live_transcript = ""
live_summary = ""
thread = None

def record_audio(duration=10):
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_wav_path = temp_wav.name
    temp_wav.close()

    command = [
        "ffmpeg", "-y",  # overwrite
        "-f", "avfoundation",
        "-i", ":1",  # Adjust this index to match your audio source (BlackHole)
        "-t", str(duration),
        "-ac", "1",
        "-ar", "16000",
        temp_wav_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return temp_wav_path

def live_loop():
    global live_running, live_transcript, live_summary
    while live_running:
        path = record_audio()
        try:
            result = model.transcribe(path)
            segment = result["text"]
            live_transcript += "\n" + segment
            prompt = f"Summarize the meeting so far and extract action items:\n{live_transcript}"
            params = {GenTextParamsMetaNames.MAX_NEW_TOKENS: 512}
            summary = inference.generate_text(prompt=prompt, params=params)
            live_summary = summary
        except Exception as e:
            print("❌ Error in live loop:", e)
        finally:
            os.remove(path)

def start_thread():
    global thread
    thread = threading.Thread(target=live_loop)
    thread.start()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/start_live', methods=['POST'])
def start_live():
    global live_running, live_transcript, live_summary
    if not live_running:
        live_running = True
        live_transcript = ""
        live_summary = ""
        start_thread()
    return '', 204

@app.route('/stop_live', methods=['POST'])
def stop_live():
    global live_running
    live_running = False
    return '', 204

@app.route('/get_updates', methods=['GET'])
def get_updates():
    return jsonify({
        "transcript": live_transcript.strip() or "No transcript yet...",
        "summary": live_summary.strip() or "No summary yet..."
    })

if __name__ == '__main__':
    app.run(debug=True)
