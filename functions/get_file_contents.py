import os

def get_file_contents(working_directory, file_path):
    wd = os.path.join(os.getcwd(), working_directory)  # Get the cwd and working directory
    file_to_access = os.path.abspath(os.path.join(wd, file_path))  # Get the directory to access in working_directory

    if not os.path.exists(file_to_access):  # If the supplied file path isn't in the WD
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_to_access):  # If the supplied file isn't a file
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    max_chars = 10000  # Max characters to read from the file
    try:
        with open(file_to_access, "r") as file:  # Open the file
            file_contents_string = file.read()  # Read the full file
            if len(file_contents_string) > max_chars:  # If the file is longer than the max_chars
                file_contents_string = file_contents_string[:max_chars] + f"[...File '{file_path}' truncated at 10000 characters]"  # Truncate the string
            return file_contents_string
    except OSError as e:
        return f'Error: {e}'
    except:
        return f'Error: An error occurred'
    