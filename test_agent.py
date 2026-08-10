import unittest
from agent_components import check_calendar, execute_tool


class TestTools(unittest.TestCase):

    def test_check_calendar_returns_string(self):
        result = check_calendar()
        self.assertIsInstance(result, str)

    def test_check_calendar_contains_standup(self):
        result = check_calendar()
        self.assertIn("standup", result)



if __name__ == "__main__":
    unittest.main()