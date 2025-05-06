#Step1: Setup GROQ API key
import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

#Step2: Convert image to required format
import base64

image_path="acne.jpg"
image_file = open(image_path, "rb")
encoded_image=base64.b64encode(image_file.read()).decode('utf-8')

#Step3: Setup Multimodal LLM
from groq import Groq

client=Groq()
query="Is there something wrong with my face?"
model="meta-llama/llama-4-scout-17b-16e-instruct"
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
    model=model,
)

print(chat_completion.choices[0].message.content)