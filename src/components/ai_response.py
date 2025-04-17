from dotenv import load_dotenv
load_dotenv()

# Requirements
import os
from src.logging import logger
import subprocess
import platform
import elevenlabs
from elevenlabs.client import ElevenLabs

# API Key init
ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")

# Transformation of text to speech using Elevenlabs
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.generate(
        text= input_text,
        voice= "Aria",
        output_format= "mp3_22050_32",
        model= "eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])
        else:
            raise OSError("Unsupported operating system")
        logger.info("Eleven labs processed the audio.")
    except Exception as e:
        logger.info(f"An error occurred while trying to play the audio: {e}")
