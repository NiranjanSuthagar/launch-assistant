import requests 
import json
from ollama import chat
from ollama import ChatResponse
import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

def generate_prompt(error_log):
    prompt = f"""
    You are the AI assistant, specific for the Launch platform from Contentstack.
    Your output should be in the following format:
    Error Location: "Stating the possible file or configuration that is raising this issue",
    Error Type: "Name of the particular error",
    Solution: "Your solution for that problem with respect to the log provided(keep this short and crisp)"
    here is your error: {error_log}
    *DONOT PROVIDE ANYTHING ADDITIONAL*
    """
    return prompt

def get_suggestion_ollama(error_log):
    prompt = generate_prompt(error_log)
    stream = chat(
        model='llama3.1:latest',
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)

def get_suggestion(error_log):
    prompt = generate_prompt(error_log)
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    chat_completion = client.chat.completions.create(
         messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-8b-instant",
    )
    
    print(chat_completion.choices[0].message.content)
    
# if __name__ == "__main__":
#     # Sample error log
#     error_log = """
#     09:33:26.582 npm error Incorrect or missing password.
#     09:33:26.584 npm error If you were trying to login, change your password, create an authentication token or enable two-factor authentication then that means you likely typed your password in incorrectly.
#     09:33:26.598 npm error probably out of date. To correct this please try logging in again with: npm login
#     """
    
#     suggestion = get_suggestion_from_llama(error_log)
#     print("Suggestion:", suggestion)
