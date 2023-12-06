import unittest
from unittest.mock import patch
from console import HBNBCommand
import os
from io import StringIO

class TestConsole(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.console = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        del cls.console

    def tearDown(self):
        try:
            os.remove("file.json")
        except Exception:
            pass

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_place(self, mock_stdout):
        self.console.onecmd("create Place")
        place_id = mock_stdout.getvalue().strip()
        self.assertTrue(place_id)

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_state(self, mock_stdout):
        self.console.onecmd("create State")
        state_id = mock_stdout.getvalue().strip()
        self.assertTrue(state_id)


if __name__ == '__main__':
    unittest.main()
