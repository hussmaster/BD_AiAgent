import os, sys, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.config import system_prompt
from functions.get_files_info import available_functions, get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.get_file_content import get_file_content



load_dotenv()
#API Key
api_key = os.environ.get("GEMINI_API_KEY")
#Client variable
client = genai.Client(api_key=api_key)

#CLI Arguments
parser = argparse.ArgumentParser()
#Sets verbose flag
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
#Grabs user prompt, looks for string on cli
parser.add_argument("prompt", type=str, help="User prompt")
#Puts args into variable
args = parser.parse_args()
#Stores messages used to communicate with Gemini
messages = [
    types.Content(role="user", parts=[types.Part(text=args.prompt)]),
]
#Dictionary of available functions
func_dict = {"get_files_info": get_files_info,
             "write_file": write_file,
             "run_python_file": run_python_file,
             "get_file_content": get_file_content
            }
#Function to handle calling the functions
def call_function(function_call_part, verbose=False):
    if function_call_part.name in func_dict:
        #Add working directory to the args dictionary
        function_call_part.args["working_directory"] = "./calculator"
        if verbose == True:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            #Grab function out of function dictionary
            func = func_dict[function_call_part.name]
            #Call function with arguments and place in function_result variable
            function_result = func(**function_call_part.args)
        else:
            func = func_dict[function_call_part.name]
            function_result = func(**function_call_part.args)
            print(f" - Calling function: {function_call_part.name}")
        #Return function result, must be a dictionary
        return types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_result}
                )
            ],
        )

    else:
        #Error handling
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"}
                )
            ],
        )

def main():
    n = 0
    print("Hello from ai-agent!")
    #Generates response
    while n < 20:
        n += 1
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]),
            )
        made_call = False
        for c in response.candidates:
            messages.append(c.content)
            for p in c.content.parts:
                if p.function_call:
                    made_call = True
                    result = call_function(p.function_call, args.verbose)
                    messages.append(types.Content(role="user", parts=[result.parts[0]]))
        if response.text:
            print(response.text)
            break

    #Gets some usage variables
    prompt_count = response.usage_metadata.prompt_token_count
    response_count = response.usage_metadata.candidates_token_count
    #If --verbose is used
    if args.verbose == True:
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {prompt_count}")
        print(f"Response tokens: {response_count}")

if __name__ == "__main__":
    main()
