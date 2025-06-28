# 🧠 Smart Meeting Summarizer

A real-time meeting transcription and summarization web app using **Whisper**, **IBM Watsonx AI**, and **Flask**. This tool captures audio from your system, transcribes it using Whisper, and summarizes the conversation with IBM's large language model.

## 🚀 Features

- 🎙 Real-time audio capture every 10 seconds  
- 📝 Transcription with OpenAI’s Whisper model  
- 📄 Summarization and action item extraction via IBM Watsonx  
- 🌐 Simple and intuitive web interface  
- 🔁 Live updates of transcript and summary  

## 📁 Project Structure

```
smart-meeting-summarizer/
├── app.py               # Flask backend logic
├── templates/
│   └── index.html       # Web UI
```

## ⚙️ Requirements

- Python 3.8+  
- `ffmpeg` (for audio capture)  
- macOS with BlackHole (or equivalent virtual audio device)  
- IBM Cloud account with Watsonx access  

## 🧰 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/smart-meeting-summarizer.git
   cd smart-meeting-summarizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install `ffmpeg` (macOS)**
   ```bash
   brew install ffmpeg
   ```

4. **Set up BlackHole**
   - Install [BlackHole](https://existential.audio/blackhole/)
   - Route Google Meet or system audio through BlackHole input

## 🔐 IBM Watsonx Setup

Edit the `app.py` file and replace with your IBM Cloud credentials:

```python
credentials = Credentials.from_dict({
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey": "your-api-key"
})
inference = ModelInference(
    model_id="ibm/granite-3-2b-instruct",
    project_id="your-project-id",
    credentials=credentials
)
```

## ▶️ Running the App

Start the Flask server:

```bash
python app.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser.

## 🧪 How It Works

1. Paste your Google Meet URL (optional for visual cue)  
2. Click “Start Live Summarization”  
3. App records 10-second audio chunks  
4. Transcription via Whisper  
5. Prompt-based summarization via IBM Watsonx  
6. Output updates in real-time  

## ⚠️ Notes

- The audio source is set to `":1"` for `ffmpeg`. Change it based on your BlackHole configuration.  
- Whisper model used: `base` (changeable to `small`, `medium`, etc.)  
- Summaries are cumulative and based on entire transcript.  

## 🖼️ Screenshot

![Smart Meeting Summarizer Screenshot](screenshots/demo.png)

## 📌 Disclaimer

This is a prototype. Do not expose your IBM API keys publicly. Ensure your use complies with IBM and OpenAI terms of service.

## 📄 License

MIT License

## 🙌 Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper)  
- [IBM Watsonx](https://www.ibm.com/watsonx)  
- [BlackHole Virtual Audio Driver](https://existential.audio/blackhole/)  
- [Flask Framework](https://flask.palletsprojects.com/)
