# src/adapters/web/server.py
from fastapi import FastAPI

from src.adapters.web.runner import Runner


class BackgroundServer:
    def __init__(self, app: FastAPI, host: str, port: int):
        self._runner = None
        self.app = app
        self.host = host
        self.port = port

    def start(self, runner: Runner):
        self._runner = runner
        return runner.start(self)

def create_server(app: FastAPI, ip: str, port: int) -> BackgroundServer:
    server = BackgroundServer(app=app, host=ip, port=port)
    return server

