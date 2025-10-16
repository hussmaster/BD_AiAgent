import os
from functions.config import MAX_CHARS


def get_file_content(working_directory, file_path):
    #Creates full path to file
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    #print(full_path)
    #Absolute path of working directory
    abs_path_wd = os.path.abspath(working_directory)
    #Checks if file is not in the working directory
    if not(full_path == abs_path_wd or full_path.startswith(abs_path_wd + os.sep)):
        error_str = (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        return error_str
    #Checks to make sure the file exists
    elif not os.path.isfile(full_path):
        error_str = (f'Error: File not found or is not a regular file: "{file_path}"')
        return error_str
    else:
        #Opens file and reads
        try:
            with open(full_path, "r") as f:
                file_content = f.read(MAX_CHARS + 1)
                if len(file_content) > MAX_CHARS:
                    content = file_content[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'
                else:
                    content = file_content
            return content
        except Exception as e:
            return f"Error: {e}"
        