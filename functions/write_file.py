import os

def write_file(working_directory, file_path, content):
    wd = os.path.join(os.getcwd(), working_directory)  # Get the cwd and working directory
    file_to_access = os.path.abspath(os.path.join(wd, file_path))  # Get the directory to access in working_directory

    if not file_to_access.startswith(wd):  # If the supplied file path isn't in the WD
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
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
