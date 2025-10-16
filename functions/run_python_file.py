import os, subprocess, sys

def run_python_file(working_directory, file_path, args=[]):
    #Creates full path to file
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    #Absolute path to working directory
    abs_path_wd = os.path.abspath(working_directory)
    #Checks if file is not in the working directory
    if not(full_path == abs_path_wd or full_path.startswith(abs_path_wd + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    elif not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    else:
        try:
            cmd = [sys.executable, full_path, *args]
            sub_output = subprocess.run(cmd, cwd=abs_path_wd, timeout=30, capture_output=True, text=True)
            parts = []
            if sub_output.stdout:
                parts.append(f"STDOUT: {sub_output.stdout}".rstrip())
            if sub_output.stderr:
                parts.append(f"STDERR: {sub_output.stderr}".rstrip())
            if sub_output.returncode != 0:
                parts.append(f"Process exited with code {sub_output.returncode}")
            if not parts:
                return "No output produced."
            return "\n".join(parts)
        except Exception as e:
            return f"Error: executing Python file: {e}"