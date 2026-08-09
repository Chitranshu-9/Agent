TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_calendar",
            "description": "Check calendar events",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_preferences",
            "description": "Get user preferences",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"}
                }
            }
        }
    }
]

def check_calendar(date=None):
    return "10am: Standup, 2pm: Dentist"

def search_web(query):
    return f"Top result for '{query}': ..."

def get_user_preferences(category):
    return f"Preferences for {category}: None"

def execute_tool(name, args):
    funcs = {
        "check_calendar": check_calendar,
        "search_web": search_web,
        "get_user_preferences": get_user_preferences
    }

    if name not in funcs:
        return f"Unknown tool: {name}"

    return funcs[name](**args)