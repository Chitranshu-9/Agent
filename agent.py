from openai import OpenAI
import os, json
from openai import OpenAI
from tools import TOOLS, execute_tool


client = OpenAI(
    base_url="https://api.openai.com/v1",
    api_key="YOUR_API_KEY"
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! Can you help me with a question?"}
    ])

response_text = response.choices[0].message.content

print("Response from OpenAI API:", response_text)


MAX_ITERATIONS = 10
SYSTEM_PROMPT = "You are a helpful assistant."
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)
def run_agent(user_message, history=None):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": user_message})

    for _ in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model="openai/gpt-4.1-mini",
            messages=messages,
            tools=TOOLS
        )

        choice = response.choices[0]

        if choice.finish_reason == "tool_calls":
            messages.append(choice.message)

            for tc in choice.message.tool_calls:
                try:
                    args = json.loads(tc.function.arguments)
                    result = execute_tool(tc.function.name, args)
                except Exception as e:
                    result = f"Error: {e}"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result
                })

        elif choice.finish_reason == "stop":
            return choice.message.content