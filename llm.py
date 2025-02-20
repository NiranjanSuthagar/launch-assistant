import requests 
import json
from ollama import chat
from ollama import ChatResponse
import os
from dotenv import load_dotenv
from groq import Groq
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

error_samples = {
    "Private Package Authentication Failure": """\
Error: 401 Unauthorized - Authentication failed for private package repository.
Attempted to fetch package from https://registry.npmjs.org/private-package.
Response: 401 Unauthorized - Invalid authentication credentials.
Ensure that your .npmrc file contains a valid authentication token.
""",
    "Private Package Authentication Failure (Token Error)": """\
Error: npm ERR! code E401
npm ERR! Unable to authenticate with the npm registry.
npm ERR! Incorrect or missing password.
npm ERR! Ensure that your authentication token is correctly set in ~/.npmrc.
""",
    "Unresolved Dependency": """\
Error: ERR! 404 Not Found - No matching version found for 'express@5.0.0'.
npm ERR! A complete log of this run can be found in: /home/user/.npm/_logs/2025-02-20T08_35_00_000Z-debug.log
Possible reasons:
- The package version does not exist in the registry.
- The package name is misspelled.
- The package has been deprecated or removed.
""",
    "Dependency Version Conflict": """\
Error: Conflicting dependencies found:
- react@17.0.2 requires react-dom@17.0.2 but react-dom@18.0.0 is installed.
Resolution:
- Run `npm ls react-dom` to check dependency tree.
- Use `npm dedupe` or manually adjust package.json to resolve conflicts.
""",
    "Incorrect Build Command Configuration": """\
Error: npm ERR! Missing script: 'build'.
npm ERR! A build script is required to compile the project.
npm ERR! Ensure that package.json contains a "scripts" section with a "build" command.
Example:
{
  "scripts": {
    "build": "webpack --mode production"
  }
}
""",
    "No Build Command Configured": """\
Error: No build command configured.
Skipping dependency installation and build steps.
Possible causes:
- No build command is defined in the deployment settings.
- The project does not require a build step.
- The build command is incorrectly specified in package.json.
""",
    "Incorrect Environment Variables Configuration": """\
Error: Missing required environment variable DATABASE_URL.
Failed to load environment variables.
Deployment logs:
- DATABASE_URL is undefined.
- Ensure that all required environment variables are set in the deployment configuration.
- Check .env files or cloud provider settings for missing values.
""",
    "Destination Exceeds Character Limit": """\
Error: destination of rewrite exceeds 256 characters.
launch.json error: length must be <= 256, but got 312 at /rewrites/2/destination.
Ensure that the destination URL is within the allowed character limit.
""",
    "No Destination for Rewrite/Redirect": """\
Error: launch.json error: missing properties: 'destination' at /rewrites/2.
Rewrite rule is missing a destination field.
Example of a correct configuration:
{
  "rewrites": [
    {
      "source": "/old-path",
      "destination": "/new-path"
    }
  ]
}
""",
    "Invalid Regex in Rewrite/Redirect": """\
Error: invalid regex in rewrite rule.
launch.json error: rewrites has invalid Destination pattern.
Ensure that the regex pattern follows valid syntax.
Example of a valid regex:
{
  "rewrites": [
    {
      "source": "^/blog/(.*)$",
      "destination": "/articles/$1"
    }
  ]
}
""",
    "Edge Function Deployment Error": """\
Error: Edge functions deployment error.
Deployment failed due to timeout while uploading function to the edge network.
Logs:
- Uploading function to edge location us-east-1...
- Connection timed out after 30 seconds.
- Retrying...
Possible solutions:
- Check network connectivity.
- Increase deployment timeout settings.
- Ensure the function size is within allowed limits.
""",
    "Edge Function Deletion Error": """\
Error: Error while deleting user edge function.
Function ID: edge-fn-12345
Logs:
- Attempting to delete function...
- Function not found in the system.
- Ensure that the function exists before attempting deletion.
""",
    "Cloud Function Deployment Error": """\
Error: Cloud function deployment failed.
Logs:
- Connecting to cloud provider...
- Uploading function code...
- Error: Unable to connect to cloud storage during deployment.
Possible causes:
- Network issues preventing connection to cloud storage.
- Incorrect cloud provider credentials.
- Insufficient permissions to deploy functions.
""",
    "Site Setup Deployment Failure": """\
Error: Deployment failed during site setup.
Logs:
- Verifying site configuration...
- Error: Configuration mismatch detected.
- Expected: Node.js 18, Found: Node.js 16.
Resolution:
- Update the runtime version in deployment settings.
- Ensure that all required dependencies are installed.
""",
    "Syntax Error": """\
Error: SyntaxError: Unexpected token '}' at index.js:45:12.
Stack trace:
  at Object.parse (native)
  at Module._compile (internal/modules/cjs/loader.js:1085:30)
Possible causes:
- Missing or extra closing brace in JSON or JavaScript file.
- Incorrect syntax in configuration files.
""",
    "Runtime Error": """\
Error: TypeError: Cannot read properties of undefined (reading 'map') at app.js:23:5.
Stack trace:
  at renderList (app.js:23:5)
  at renderComponent (app.js:45:10)
Possible solutions:
- Ensure that the variable being accessed is properly initialized.
- Add null checks before calling `.map()` or other methods.
"""
}

def generate_prompt(user_input):
    prompt = f"""
    You are the AI assistant, specific for the Launch platform from Contentstack.
    Your output should be in the following format:
    
    - **Error Location:** `Stating the possible file or configuration that is raising this issue`
    - **Error Type:** `Name of the particular error`
    - **Solution:** "Your solution for that problem with respect to the log provided (keep this short and crisp)"
    
    Here is your error: {user_input}
    *use `file-name` this format for file names and important phrases
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