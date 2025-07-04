import os
from google.genai import types

def write_file(working_directory, file_path, content):
    wd = os.path.abspath(os.path.join(os.getcwd(), working_directory))  # Get the cwd and working directory, abspath is used to handle . and non-full addresses
    file_to_access = os.path.abspath(os.path.join(wd, file_path))  # Get the directory to access in working_directory

    if not file_to_access.startswith(wd):  # If the supplied file path isn't in the WD
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory {file_to_access} - {wd}'
    
    if not os.path.exists(file_to_access):  # If the supplied file doesn't exist
        dirname = os.path.dirname(file_to_access)  # Get the final directory path
        if not os.path.exists(dirname):  # If the directory does not exist
            try:
                os.makedirs(dirname)  # Make the directories (including intermediate directories)
            except OSError as e:
                return f'Error: {e}'
            except:
                return f'Error: An Error Occurred'

    try:
        with open(file_to_access, 'w') as file:  # Open or create the file
            file.write(content)  # Write the content to the file
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except OSError as e:
            return f'Error: {e}'
    except:
            return f'Error: An Error Occurred'

# Create a schema to explain how write_file is used
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the content to the file specified in file_path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path that leads to the specific file that content will be written to, relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written to the file from file_path",
            )
        },
    ),
)
