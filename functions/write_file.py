import os

def write_file(working_directory, file_path, content):
    #Creates full path to file
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    #Absolute path of working directory
    abs_path_wd = os.path.abspath(working_directory)
    #Checks if file is not in the working directory
    #print(full_path)
    #print(abs_path_wd)
    if not(full_path == abs_path_wd or full_path.startswith(abs_path_wd + os.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not(os.path.exists(full_path)):
        try:
            with open(full_path, "w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f"Error: {e}"
    else:
        try:
            with open(full_path, "w") as f:
                f.write(content)
            return f'Successfully wroe to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f"Error: {e}"
