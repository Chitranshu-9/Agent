import os
import json
from openai import OpenAI


MEMORY_FILE = "/agent_memory.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)

    return {}


def save_memory(memory):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def save_preference(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)
    return f"Saved: {key} = {value}"


tools = [
    # ... check_calendar ...,
    {
        "type": "function",
        "function": {
            "name": "save_preference",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string"
                    },
                    "value": {
                        "type": "string"
                    }
                },
                "required": ["key", "value"]
            }
        }
    }
]

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)


MAX_ITERATIONS = 10


def check_calendar(date):
    return f"Standup 9am, Review 2pm on {date}"


memory = load_memory()

args = {
    "date": "Thursday"
}


for _ in range(MAX_ITERATIONS):
    try:
        result = check_calendar(args["date"])
        print(result)

        memory["last_calendar_check"] = {
            "date": args["date"],
            "result": result
        }

        save_memory(memory)
        break

    except Exception as e:
        result = f"Tool error: {e}"
        print(result)
        
