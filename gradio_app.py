from dotenv import load_dotenv
load_dotenv()

# Requirements
import os
import gradio as gr
from src.logging import logger
from src.components.process import encode_image, analyze_image_with_query
from src.components.Query_fetch import transcribe_with_groq
from src.components.ai_response import text_to_speech_with_elevenlabs

# AI main Prompt

system_prompt = """
Act as a versatile expert analyzing images and queries—adapt your expertise to match the task, whether medical, technical, or visual. 
With what I see, I think you have [specific observation], and here’s what that means [concise insight]. 
Respond naturally like a human specialist, avoiding AI jargon, markers, or numbered lists—just direct, empathetic answers in one or two sentences max.
skip the disclaimers. Just the facts, clear and quick.
"""
 
# Function for processing inputs: audio_filepath, image_filepath from the UI

def process_inputs(audio_filepath, image_filepath):
    # Handle the output audio to text 
    speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                                                 audio_filepath=audio_filepath,
                                                 stt_model="whisper-large-v3")
    logger.info("Audio and image recieved. Send for transcription.")
    

    # Handle the image input
    if image_filepath:
        ai_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="llama-3.2-11b-vision-preview")
    else:
        ai_response = "No image provided for me to analyze"

    logger.info("Image provided to the AI. Processing the response...")

    # Handle the output voice
    voice_of_ai = text_to_speech_with_elevenlabs(input_text=ai_response, output_filepath="final.mp3") 

    logger.info("Recieved the final AI response.")
    
    return speech_to_text_output, ai_response, voice_of_ai


# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Ai's Response"),
        gr.Audio("Temp.mp3")
    ],
    title="AI Vision and Voice Assistant"
)

iface.launch(debug=True)