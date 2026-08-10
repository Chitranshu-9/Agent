from openai import OpenAI
import os
import json
import time


# =========================
# Configuration
# =========================

model = "openai/gpt-4.1-mini"
MAX_ITERATIONS = 10


# =========================
# OpenAI Client
# =========================

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)


# =========================
# Runtime State
# =========================

run_log = []

total_prompt_tokens = 0
total_completion_tokens = 0
iteration_count = 0


# =========================
# Tool Execution
# =========================

def execute_tool(name, args):
    start_time = time.time()

    try:
        if name == "check_calendar":
            result = check_calendar(**args)
        else:
            result = f"Unknown tool: {name}"

    except Exception as e:
        result = f"Error: {str(e)}"

    duration = time.time() - start_time

    run_log.append(
        {
            "tool": name,
            "args": args,
            "result": str(result)[:100],
            "duration_ms": round(duration * 1000, 2),
        }
    )

    return result


# =========================
# Agent Loop
# =========================

wall_start = time.time()

for iteration in range(MAX_ITERATIONS):

    iteration_count += 1

    if iteration_count >= MAX_ITERATIONS - 2:
        print(
            f"WARNING: approaching iteration limit "
            f"({iteration_count}/{MAX_ITERATIONS})"
        )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
    )

    # Track token usage
    if response.usage:
        total_prompt_tokens += response.usage.prompt_tokens
        total_completion_tokens += response.usage.completion_tokens

    # Check whether the model requested a tool
    if response.choices[0].message.tool_calls:

        for tool_call in response.choices[0].message.tool_calls:

            tool_name = tool_call.function.name

            tool_args = json.loads(
                tool_call.function.arguments
            )

            result = execute_tool(
                tool_name,
                tool_args,
            )

            print(
                f"Tool called: {tool_name}"
            )

            print(
                f"Result: {result}"
            )

    else:
        # Final response
        print(
            response.choices[0].message.content
        )
        break


# =========================
# Execution Summary
# =========================

elapsed = round(
    time.time() - wall_start,
    2,
)

print("\n=== Execution Summary ===")

print(
    f"Iterations used: "
    f"{iteration_count}/{MAX_ITERATIONS}"
)

print(
    f"Total tokens: "
    f"{total_prompt_tokens + total_completion_tokens}"
)

print(
    f"Tools called: "
    f"{len(run_log)}"
)

for entry in run_log:
    print(
        f" - {entry['tool']}: "
        f"{entry['duration_ms']}ms"
    )

print(
    f"Wall-clock time: "
    f"{elapsed}s"
)