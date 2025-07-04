import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_contents import schema_get_file_content, get_file_contents
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file


def call_function(function_call_part, verbose=False):
    '''
    Runs the functions the LLM wants to execute
    '''
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    arguments = function_call_part.args  # Get the arguments it wants to pass to the function
    arguments['working_directory'] = './calculator'  # Add the WD as the LLM is not permitted to set this

    # For each function available to the LLM execute the function with arguments for it
    if function_call_part.name == "get_files_info":
        result = get_files_info(**arguments)
    elif function_call_part.name == "get_file_contents":
        result = get_file_contents(**arguments)
    elif function_call_part.name == "run_python_file":
        result = run_python_file(**arguments)
    elif function_call_part.name == "write_file":
        result = write_file(**arguments)
    else:  # If the LLM tried to call a non-existent function let it know the error
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )
    # Return the results of running the function to the LLM
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,  # Name of the function executed
                response={"result": result},  # Results of running the function
            )
        ],
    )
    


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)  # Create instance of Gemini Client

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# State what functions are available to the LLM
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

# If no prompt is provided kill the program
if len(sys.argv) < 2:
    print('ERROR: No prompt provided')
    sys.exit(1)

user_prompt = sys.argv[1]  # Get the first argument provided by the user

# Store the user prompt in the messages list
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]


# Run max 20 prompts to avoid exceeding the free limits
for i in range(0,20):
    # Get a response to the prompt from the specified AI model
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))  # Passes a config to the agent

    # If a response is returned by the model
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)  # Add every response to the message log for context

    # Check for a verbose flag
    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":  # If it's the verbose flag
            print(f'User prompt: {user_prompt}')
            print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
            print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
        

    if response.function_calls:  # If the LLM wants to make any function calls
        print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
        result = call_function(response.function_calls[0])  # Call "call_function" to execute the function and get a response
        try:
            if result.parts[0].function_response.response:  # If the response returned okay
                messages.append(result)  # Add the response to the messages log
                if len(sys.argv) > 2:
                    if sys.argv[2] == "--verbose":  # Check for the verbose flag
                        print(f"-> {result.parts[0].function_response.response}")  # Display the results to user
        except:
            raise Exception(f'Error occured in function: {response.function_calls[0].name}')
    else:  # No more functions called, model is finished
        print(response.text)  # Display final response
        break

