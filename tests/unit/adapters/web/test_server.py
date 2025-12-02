# test/unit/adapters/web/test_server.py
import unittest
from unittest.mock import create_autospec

from src.adapters.web.app import create_app
from src.adapters.web.runner import Runner
from src.adapters.web.server import create_server


class TestServer(unittest.TestCase):
    def test_create_server_wires_dependencies(self):
        app = create_app()
        server = create_server(app, "127.0.0.1", 80)

    def test_start_calls_runner(self):
        app = create_app()
        server = create_server(app, "127.0.0.1", 80)

        mock_runner = create_autospec(Runner, instance=True)

        # simulate a return value from start
        mock_runner.start.return_value = {"handle": "fake"}

        handle = server.start(runner=mock_runner)

        mock_runner.start.assert_called_once_with(server)

        self.assertIs(handle, mock_runner.start.return_value)
        self.assertIs(server._runner, mock_runner)
