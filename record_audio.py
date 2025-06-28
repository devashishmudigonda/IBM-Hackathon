import sounddevice as sd
import soundfile as sf

duration = 60  # seconds
filename = "live_meeting.wav"
samplerate = 16000  # Whisper's preferred rate
channels = 1

# List all audio devices
print("\nAvailable input devices:\n")
print(sd.query_devices())

# Find BlackHole
device_name = "BlackHole"
input_device = None
for idx, device in enumerate(sd.query_devices()):
    if device_name in device['name'] and device['max_input_channels'] > 0:
        input_device = idx
        print(f"✅ Using device #{idx}: {device['name']}")
        break

if input_device is None:
    raise RuntimeError("BlackHole input device not found!")

print("🎙️ Recording... Speak or play Meet audio.")

# Record audio
recording = sd.rec(
    int(duration * samplerate),
    samplerate=samplerate,
    channels=channels,
    dtype='int16',
    device=input_device
)
sd.wait()

# Save to file
sf.write(filename, recording, samplerate)
print(f"✅ Saved recording as {filename}")
