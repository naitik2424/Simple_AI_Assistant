#standard library imports
import os
#Third-party import
from openai import OpenAI
from dotenv import load_dotenv
#local modules
from tools import TOOLS,run_tool
from Utilities.utilities import log


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
    user_input = input("\n 🧑 Naitik : ")
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

        log(f"Step {step+1} : model requested{len(msg.tool_calls)} tool calls")
        messages.append(msg)

        for tool_call in msg.tool_calls:
            result = run_tool(tool_call)
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
                        "role" : "assistant",
                        "content" : fallback,
        })
        print("🤖 Assistant: "+ fallback)
        continue
        
    messages.append({
        "role":"assistant",
        "content": msg.content,
    })
    print("🤖 Assistant: " + (msg.content  or ""))()