# from ibm_watsonx_ai.foundation_models import ModelInference
# from ibm_watsonx_ai.metanames import GenTextParamsMetaNames
# from ibm_watsonx_ai import Credentials

# credentials = Credentials.from_dict({
#     "url": "https://us-south.ml.cloud.ibm.com",
#     "apikey": "eUtvlc1m_NxqEJGX5nof07Y-TIISdJBKyUrEwK1vkYTd"
# })

# inference = ModelInference(
#     # model_id="ibm/granite-3-3-8b-instruct",
#     model_id = "ibm/granite-3-2b-instruct",  # Lighter, usually under less load

#     project_id="6f6af590-901e-4508-ae02-8a3ecf7498d1", 
#     credentials=credentials
# )

# with open("transcript.txt", "r") as f:
#     transcript = f.read()

# prompt = f"Summarize the following meeting and extract all action items with responsible person and deadline:\n\n{transcript}"

# params = {
#     GenTextParamsMetaNames.MAX_NEW_TOKENS: 512,
#     GenTextParamsMetaNames.TEMPERATURE: 0.7
# }

# response = inference.generate_text(prompt=prompt, params=params)

# print("✅ Output:\n")
# print(response)

# with open("output.txt", "w") as f:
#     f.write(response)




import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import tempfile
import os

from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames
from ibm_watsonx_ai import Credentials

# Step 1: Record audio
def record_audio(duration=10, filename="temp_audio.wav"):
    fs = 16000  # Sampling rate
    print("🎤 Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    write(filename, fs, audio)
    print("✅ Recording saved as", filename)
    return filename

# Step 2: Transcribe with Whisper
def transcribe_audio(filepath):
    print("🧠 Transcribing...")
    model = whisper.load_model("base")
    result = model.transcribe(filepath)
    print("📝 Transcript:", result["text"])
    return result["text"]

# Step 3: Summarize with WatsonX
def summarize_with_ibm(transcript):
    credentials = Credentials.from_dict({
        "url": "https://us-south.ml.cloud.ibm.com",
        "apikey": "eUtvlc1m_NxqEJGX5nof07Y-TIISdJBKyUrEwK1vkYTd"
    })

    inference = ModelInference(
        model_id="ibm/granite-3-2b-instruct",  # Smaller model
        project_id="6f6af590-901e-4508-ae02-8a3ecf7498d1",
        credentials=credentials
    )

    prompt = f"Summarize the following meeting and extract all action items with responsible person and deadline:\n\n{transcript}"
    params = {
        GenTextParamsMetaNames.MAX_NEW_TOKENS: 512,
        GenTextParamsMetaNames.TEMPERATURE: 0.7
    }

    response = inference.generate_text(prompt=prompt, params=params)
    return response

# Step 4: Main workflow
if __name__ == "__main__":
    audio_file = record_audio(duration=10)
    transcript = transcribe_audio(audio_file)
    summary = summarize_with_ibm(transcript)

    print("\n📌 Final Summary:\n", summary)

    with open("output.txt", "w") as f:
        f.write(summary)

    os.remove(audio_file)  # optional cleanup
