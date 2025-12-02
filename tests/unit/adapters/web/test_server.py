import unittest

from src.adapters.web.app import create_app
from src.adapters.web.server import create_server


class TestServer(unittest.TestCase):
    def test_create_server_wires_dependencies(self):
        # detroit style the uvicorn app. just dont call or actually start it.
        app = create_app()
        server = create_server(app, "127.0.0.1", 80)


if __name__ == '__main__':
    unittest.main()
