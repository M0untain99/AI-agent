import os
from google.genai import types

def get_files_info(working_directory, directory='.'):
    wd = os.path.abspath(os.path.join(os.getcwd(), working_directory))  # Get the cwd and working directory
    dir_to_access = os.path.abspath(os.path.join(wd, directory))  # Get the directory to access in working_directory

    # If the supplied directory is just the WD itself
    if wd == dir_to_access:
        pass  # That's fine
    elif directory not in os.listdir(wd):  # If the supplied directory isn't in the WD
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # If the supplied directory is NOT a directory
    if not os.path.isdir(dir_to_access):
        return f'Error: "{directory}" is not a directory'
    
    try:
        contents = os.listdir(dir_to_access)  # Get the contents of the dir as a list
        file_info = []
        
        for file in contents:
            file_path = os.path.join(dir_to_access, file)  # Create the file path
            info = f'- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}'  # Get the file info
            file_info.append(info)  # Add the info string to the list of file info

        output = "\n".join(file_info)  # Join the list into one string separated by new lines

        return output
    except Error as e:
        return f'ERROR: {e}'

# Create a schema to explain how the get_files_info is used
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)