# speech_models

This project demonstrates speech-to-text (stt) and text-to-speech (tts). It makes use of freely available machine learning models, so no API keys are required. Since the models run locally, the speed of the tts and sst conversions will depend on your computer, though they should run fine on any modest system.

The code was tested on a Windows system, though it was written to be compatible with Mac or Linux as well. If you encounter any problems, feel free to open an issue.

## Text to speech (tts.py)

The tts.py page uses [Silero v3](https://github.com/snakers4/silero-models) audio models for text-to-speech, and [simpleaudio](https://github.com/hamiltron/py-simple-audio) for audio playback.

## Speech to text (stt.py)

The stt.py page uses [pvrecorder](https://github.com/Picovoice/pvrecorder/tree/main/sdk/python) for recording audio, and the OpenAI [whisper](https://github.com/openai/whisper) model for transcription.

## Features

### tts

- Launch the tts.py page, and a default string from the code will be read aloud. Optionally enter a command line argument (--text "your text here") and that will be used. A random voice will be used each time, or see other [command line options](###-text-to-speech) below to specify a specific voice. 

### stt

- Launch the stt.py page, and once the message that audio is recording appears, speak to your computer and it will be transcribed to text, then printed to the console.

## Installation and setup

To run this project, you'll need Python installed on your machine. You can install from [python.org](https://www.python.org/downloads/).

## Clone the repository
```console
git clone https://github.com/dmisino/speech_models.git
cd speech_models
```

### Whisper

The OpenAI whisper module requires [ffmpeg](https://ffmpeg.org/), which must be fully installed. You may also need [Rust](https://www.rust-lang.org/) installed. See the [whisper github page](https://github.com/openai/whisper#setup) for more details.

If you have properly installed the whisper and it's dependencies, you can test it with the following commands. The wav file referenced is included with this repo, and it taken from [Open Speach Repository](https://www.voiptroubleshooter.com/open_speech/american.html). The sentences contained in the file may be viewed [here](https://www.cs.columbia.edu/~hgs/audio/harvard.html), as "list 3" for the specific audio file included in the sample folder.

```console
# Try using whisper to transcribe audio to text 
whisper "sample\OSR_us_000_0012_8k.wav" --model tiny  --language en

# Try using gpu
whisper "sample\OSR_us_000_0012_8k.wav" --model tiny  --language en --device cuda
```

When using OpenAI Whisper for speech-to-text, the provided code will use a gpu if available, but this requires a gpu-enabled version of [pytorch](https://pytorch.org/). If you already have pytorch installed, you would need to uninstall and then add the gpu-enabled version if you would like it to use your gpu for stt transcription:

```console
pip uninstall torch
pip cache purge 
pip install torch -f https://download.pytorch.org/whl/torch_stable.html
```

## Usage
 
 To run speech-to-text or text-to-speech, run the appropriate page:

 ```console
python stt.py
# or
python tts.py
 ```

## Command line options

### Text-to-speech

The text-to-speech page (tts.py) has a few command line options available. All are optional.

By default a random english speaker is selected. You may specify a different language, model and speaker. To specify these using valid options, see [silero models and speakers](https://github.com/snakers4/silero-models#models-and-speakers). Go [here](https://oobabooga.github.io/silero-samples/) to listen to samples of the 118 different available english speakers.

```console
rem tts.py command line options

rem Specify specific text to be read.
python tts.py --text "<your text here>"

rem Choose language. Default is "en".
python tts.py --language "<language>"

rem Specify model. Default is "v3_en".
python tts.py --model "<model>"

rem Specify voice used. Default is "random".
python tts.py --speaker "<speaker>"

rem Example specifying Russian, with speaker "xenia" and Russian text
python tts.py --language "ru" --model "v3_1_ru" --speaker "xenia" --text "Это какой-то русский текст, озвученный моделью машинного обучения. Доступно несколько языков, но русский звучит круто."
```

### Speech-to-text

The speech-to-text (stt.py) page has one available command line argument to change the whisper model used. There are [5 options](https://github.com/openai/whisper#available-models-and-languages) available, with differences in size, memory requirements and speed. The default model used is "tiny" which is fastest and with the lowest resource requirements.

```console
rem stt.py command line options

rem Specify model to use among options [tiny, base, small, medium, large].
python stt.py --model "<model option>"
```