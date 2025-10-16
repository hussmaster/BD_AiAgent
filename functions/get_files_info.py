import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    #Builds full path, joins working and directory and then creates absolute path
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    #Gets absolute path of working directory
    abs_path_wd = os.path.abspath(working_directory)

    if directory == ".":
        print("Result for current directory:")
    else:
        print(f"Result for '{directory}' directory")
    #Checks if full path is equal or starts with working directory
    if not (full_path == abs_path_wd or full_path.startswith(abs_path_wd + os.sep)):
        error_str = (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return error_str
    #Checks if full path is not a directory
    elif not os.path.isdir(full_path):
        error_str = (f'Error: "{directory}" is not a directory')
        return error_str
    else:
        #Lists out directory of full path
        dir_out = os.listdir(full_path)
        return_list = []
        #Loops directory
        for d in dir_out:
            return_list.append(f"- {d}: file_size={os.path.getsize(os.path.join(full_path, d))}, is_dir={os.path.isdir(os.path.join(full_path, d))}")
        #Joins list on new line
        joined = "\n".join(return_list)
        return joined
    

#Schema/Declaration for LLM
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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to list the contents from, relative to the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Arguments for the python file."
            )
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write or overwrite to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file."
            )
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
    ]
)
