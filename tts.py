import os
import sys
import io
import torch
import soundfile as sf
import simpleaudio as sa
import time
import utils
import sys

utils.clear_screen()

# Defaults. See https://github.com/snakers4/silero-models#models-and-speakers for available languages and models for each.
silero_language = "en"
silero_model = "v3_en"
silero_speaker = "random"  # Samples of available english voices: https://oobabooga.github.io/silero-samples/
speaker_name = "AI Assistant"
input_text = "Text to speach is working. If you would like to specify the text to say, call this page with the dash dash text argument. The voice has been selected at random. To choose a specific voice, use the dash dash speaker argument. Please see the read me file for more details."

# Retrieve command line arguments
args = sys.argv

try:
  n = len(sys.argv)
  #if n == 1:
  #  # No arguments passed
  for i in range(1, n):
    arg = sys.argv[i]
    if not arg.startswith("--"):
      continue 
    elif arg == "--text":
      input_text = sys.argv[i+1]
    elif arg == "--speaker":
      silero_speaker = sys.argv[i+1]
    elif arg == "--language":
      silero_language = sys.argv[i+1]
    elif arg == "--model":
      silero_model = sys.argv[i+1]      
except:
  print("Error processing command line arguments")
  exit()

silero_model_file = f"{silero_language}/{silero_model}.pt"
silero_model_file_local = f"model\{silero_model_file}".replace("/","\\")

# Make model directories if not present
utils.make_folders(f"model\{silero_language}")

device = torch.device('cpu')
torch.set_num_threads(4)

sample_rate = 48000 # [8000, 24000, 48000]

# TODO: Add optional sound effects like room reverb to match speakers environment

if not os.path.isfile(silero_model_file_local):
  print('Downloading audio model for first use')
  torch.hub.download_url_to_file(f"https://models.silero.ai/models/tts/{silero_model_file}", silero_model_file_local)  
  print(f"Download complete to local file {silero_model_file_local}") 

model = torch.package.PackageImporter(silero_model_file_local).load_pickle("tts_models", "model")
model.to(device)

def text_to_speech(text=input_text, speaker=silero_speaker):
  # Save the original stdout, and redirect to prevent other modules writing to the console
  original_stdout = sys.stdout
  sys.stdout = open(os.devnull, 'w')

  audio_tensor = model.apply_tts(text=text, speaker=speaker, sample_rate=sample_rate)
  audio_tensor_np = audio_tensor.clone().detach().numpy()

  # Convert from tensor object to bytes stored in a file buffer
  file_buffer = io.BytesIO()
  sf.write(file_buffer, audio_tensor_np, sample_rate, format='wav')
  bytes_object = file_buffer.getvalue()

  # Play audio from buffer
  sa.play_buffer(bytes_object, 1, 2, sample_rate)
  
  # Calculate the the rate at which we should display words on the screen
  duration_seconds = len(audio_tensor) / sample_rate
  words = text.split()
  time_delay = duration_seconds / len(words)

  # Turn writing to the console back on
  sys.stdout = original_stdout

  # Loop through each word and print it with a calculated time delay
  print(f"{speaker_name}: ", end="")
  for word in words:
      print(word, end=' ', flush=True)  # Print the word with a space separator and flush the output
      time.sleep(time_delay)  # Pause for the time delay

  print('\n')  # Print two newlines after all words are printed
  
  file_buffer.close()

text_to_speech(input_text)