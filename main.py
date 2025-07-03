import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)  # Create instance of Gemini Client

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# State what functions are available to the LLM
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info
    ]
)

# If no prompt is provided kill the program
if len(sys.argv) < 2:
    print('ERROR: No prompt provided')
    sys.exit(1)

user_prompt = sys.argv[1]

# Store the user prompt in the messages list
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

# Get a response to the contents prompt from the specified AI model
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))  # Passes a config to the agent

# If a value is provided after the prompt
if len(sys.argv) > 2:
    if sys.argv[2] == "--verbose":  # If it's the verbose flag
        print(f'User prompt: {user_prompt}')
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
elif response.function_calls:  # If the LLM wants to make any function calls
    print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
else:  # If there is just the prompt
    print(response.text)  # Print the text output
    
