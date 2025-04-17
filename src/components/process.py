from dotenv import load_dotenv
load_dotenv()

# Requirements
import os
import base64 
from groq import Groq
from src.logging import logger

# Key init
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")

# Encoding the image in base64 format
def encode_image(image_path):
    try:   
        image_file=open(image_path, "rb")
        return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception:
        logger.info("Image not encoded")

# LLM Model 
model="llama-3.2-90b-vision-preview"

# Providing the image and query to the model
def analyze_image_with_query(query, model, encoded_image):
    client=Groq()  
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }]
    chat_completion=client.chat.completions.create(
        messages=messages,
        model=model
    )
    logger.info("The Image and query is being processed.")
    return chat_completion.choices[0].message.content