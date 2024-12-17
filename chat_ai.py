import openai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
openai.api_key = api_key; 

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You help me write emails"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
