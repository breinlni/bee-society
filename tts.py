import os
from datetime import datetime

import playsound
from google.cloud import texttospeech


def play_text(tts_client, text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="de", name='de-DE-Wavenet-B')
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    date_string = datetime.now().strftime("%d%m%Y%H%M%S")
    filename = "voice" + date_string + ".mp3"

    with open(filename, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written as mp3')

    play_and_delete_mp3(filename)


def play_and_delete_mp3(filename):
    playsound.playsound(filename)
    os.remove(filename)
