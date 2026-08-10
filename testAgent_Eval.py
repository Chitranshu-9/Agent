import os
import unittest
from openai import OpenAI

from agent_components import CHECK_CALENDAR_TOOL


class TestAgentEval(unittest.TestCase):

    def test_agent_responds_to_calendar_query(self):
        client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            base_url=os.environ.get("OPENAI_API_BASE")
        )

        response = client.chat.completions.create(
            model="openai/gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": "What's on my calendar?"
                }
            ],
            tools=[CHECK_CALENDAR_TOOL]
        )

        choice = response.choices[0]

        made_tool_call = choice.finish_reason == "tool_calls"

        has_keyword = any(
            word in (choice.message.content or "").lower()
            for word in ["calendar", "meeting", "standup"]
        )

        self.assertTrue(made_tool_call or has_keyword)


if __name__ == "__main__":
    unittest.main()