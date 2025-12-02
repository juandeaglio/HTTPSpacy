# src/adapters/web/server.py
from fastapi import FastAPI


class BackgroundServer:
    def __init__(self, app: FastAPI, host: str, port: int):
        self.app = app
        self.host = host
        self.port = port


def create_server(app: FastAPI, ip: str, port: int) -> BackgroundServer:
    server = BackgroundServer(app=app, host=ip, port=port)
    return server

