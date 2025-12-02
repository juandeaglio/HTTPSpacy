# src/adapters/web/runner.py
import threading
from abc import ABC, abstractmethod
from typing import NamedTuple

import uvicorn


class ServerHandle(NamedTuple):
    thread: threading.Thread
    uvicorn_server: uvicorn.Server


class Runner(ABC):
    @abstractmethod
    def start(self, server) -> ServerHandle:
        """Start the server; return a handle (or anything)."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop the server."""
        pass
