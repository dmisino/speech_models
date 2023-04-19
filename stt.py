import struct
import wave
import sounddevice as sd
from pvrecorder import PvRecorder
import keyboard
import whisper
import torch
import utils
import sys

file_name = "temp/stt_input.wav"  # File name to store incoming audio 
model = "tiny"

utils.clear_screen()

# Retrieve command line arguments
args = sys.argv

try:
  n = len(sys.argv)
  for i in range(1, n):
    arg = sys.argv[i]
    if not arg.startswith("--"):
      continue 
    elif arg == "--model":
      model = sys.argv[i+1]
except:
  print("Error processing command line arguments")
  exit()

# Make temp directory for storing audio input if not present
utils.make_folders(f"temp")

try:
    # Record audio from default input device (-1) until key press
    print("Recording audio. Press [space bar] key to end recording.")
    recorder = PvRecorder(device_index=-1, frame_length=512)
    audio_data = []
    
    recorder.start()
    while True:
        frame = recorder.read()
        audio_data.extend(frame)
        if keyboard.is_pressed('space'):
            break

    recorder.stop()
    with wave.open(file_name, 'w') as f:
        f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
        f.writeframes(struct.pack("h" * len(audio_data), *audio_data))
        f.close()
    recorder.delete()

except Exception as e:
    print(f"Error recording audio: {e}")
    exit(1)

print(f"Transcribing audio using whisper '{model}' model...")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model(model).to(device)
result = model.transcribe(file_name, fp16=False, language='English')
print(result["text"])