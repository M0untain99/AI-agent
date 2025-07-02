import os
import subprocess

def run_python_file(working_directory, file_path):
    wd = os.path.join(os.getcwd(), working_directory)  # Get the cwd and working directory
    file_to_access = os.path.abspath(os.path.join(wd, file_path))  # Get the directory to access in working_directory

    if not file_to_access.startswith(wd):  # If the supplied file path isn't in the WD
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(file_to_access):  # If the supplied file doesn't exist
        return f'Error: File "{file_path}" not found.'

    if file_path[-3:] != ".py":  # If the file is not a .py file
        return f'Error: "{file_path}" is not a Python file.'

    try:
        # Run the command in the list "python 3 example/example/script.py" in the working directory specified
        output = subprocess.run(['python3', file_path], timeout=30, capture_output=True, cwd=wd)

        if output:  # If there is a result
            formatted_output = f'STDOUT: {output.stdout}\nSTDERR: {output.stderr}'  # Get output and error text
            if output.returncode != 0:  # If it exits with something other than 0
                formatted_output = f'{formatted_output}\nProcess exited with code {output.returncode}'
            return formatted_output
        else:
            return 'No output produced'
    except Exception as e:
        return f'Error: executing Python file: {e}'