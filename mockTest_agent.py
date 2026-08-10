import unittest
import json
from unittest.mock import MagicMock

from agent_components import execute_tool


class TestAgentLoop(unittest.TestCase):

    def test_tool_dispatch_on_tool_call(self):
        fake_tool_call = MagicMock()
        fake_tool_call.function.name = "check_calendar"
        fake_tool_call.function.arguments = json.dumps({})

        fake_message = MagicMock()
        fake_message.finish_reason = "tool_calls"

        name = fake_tool_call.function.name
        args = json.loads(fake_tool_call.function.arguments)

        execute_tool(name, args)

        self.assertEqual(name, "check_calendar")


if __name__ == "__main__":
    unittest.main()