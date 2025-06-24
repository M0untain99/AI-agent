import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)  # Create instance of Gemini Client

# If no prompt is provided kill the program
if len(sys.argv) < 2:
    print('ERROR: No prompt provided')
    sys.exit(1)

user_prompt = sys.argv[1]

# Store the user prompt in the messages list
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

# Get a response to the contents prompt from the specified AI model
response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages)

# If a value is provided after the prompt
if len(sys.argv) > 2:
    if sys.argv[2] == "--verbose":  # If it's the verbose flag
        print(f'User prompt: {user_prompt}')
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
else:  # If there is just the prompt
    print(response.text)  # Print the text output
