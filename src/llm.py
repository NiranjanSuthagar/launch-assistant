import requests 
import json
from ollama import chat
from ollama import ChatResponse
import os
from dotenv import load_dotenv
from groq import Groq
from src
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def get_suggestion_ollama(error_log): #for testing with local llms
    prompt = generate_prompt(error_log)
    stream = chat(
        model='llama3.1:latest',
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)

def generate_prompt(user_input,knowledge_chucks):
    prompt = f"""
    You are the AI assistant, specific for the Launch platform from Contentstack.
    Your output should be in the following format:
    
    - **Error Location:** `Stating the file or configuration that is raising this issue from the error.(if you cant find the location just say "Unknown")`
    - **Error Type:** `Name of the particular error`
    - **Solution:** "Your solution for that problem with respect to the log provided (keep this short and crisp)"
    
    Here is your error: {user_input}
    You can also refer these Relevant Chucks: {knowledge_chucks}

    *use `filename` this format for file names and important phrases
    *if the above text does not seem to be an error, Say I'm here to only assist with error logs
    
    *DO NOT PROVIDE ANYTHING ADDITIONAL*
    """
    return prompt.strip()

def get_ai_response(user_input):

    prompt = generate_prompt(user_input)
    
    response_text = ""
    for chunk in client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    ):
        if chunk.choices:
            content = chunk.choices[0].delta.content
            if content:
                response_text += content
                yield content