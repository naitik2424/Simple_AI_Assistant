from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS,FUNCTION_NAME_TO_FUNCTION_MAP
import os
import json

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)
messages= []

#Safety limit: the max number of model rounds for ONE user question
MAX_STEPS= 5
messages.append(
    {
        "role": "system",
        "content": "Act like a very humble agent and respond always under 20 words."
    }
)

#chat loop start here
while True:
    user_input = input("\nNaitik: ")
    if user_input.lower() in ["exit","quit","bye"]:
        break
    messages.append(
        {
            "role": "user",
            "content": user_input 
        }
    )
    #Chained tool calling
    for step in range(MAX_STEPS): 
        response = client.chat.completions.create(
                model=os.getenv("MODEL"),
                messages=messages,
                tools= TOOLS
            )
        msg = response.choices[0].message
        if not msg.tool_calls:
            break

        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name =tool_call.function.name
            func_args={}
            try:
                func_args = json.loads(tool_call.function.arguments or "{}")
                fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
                result= fn(**func_args)
            except Exception as e:
                result = f"Error while running {func_name}: {e}"  "
            messages.append({
                "role" : "tool",
                "tool_call_id" : tool_call.id,
                "content" : str(result),
            })

    else:
        # In python, else after a for loop runs only if the loop finishes normally,
        # meaning it wasn't ended early by a break.
        #Ran out of steps : The model never gave the final answer
        fallback = "Sorry, I could not finish this within the step limit"
        messages.append({
                        "role" : "tool",
                        "tool_call_id" : tool_call.id,
                        "content" : str(result),
        })
        print("Assistant: "+ fallback)
        continue
        
    messages.append({
        "role":"assistant",
        "content": msg.content
    })
    print("Assistant: " + msg.content)