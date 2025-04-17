from dotenv import load_dotenv
load_dotenv()

# Requirements
from src.logging import logger
from groq import Groq

# Audio Transcription Func
def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    client=Groq(api_key=GROQ_API_KEY)
    
    audio_file=open(audio_filepath, "rb")
    transcription=client.audio.transcriptions.create(
        model=stt_model,
        file=audio_file,
        language="en"
    )
    logger.info("Audio is Transcribed")
    return transcription.text