# tests/acceptance/test_server_sentence.py
import threading
import unittest
import requests
import uvicorn
from fastapi import FastAPI

from pydantic import BaseModel
from typing import List

from src.adapters.web.inbound.fastapi.message_routes import MessageRoutes


class IpsumResponseModel(BaseModel):
    sentences: List[str]


class IpsumHttpClient:
    ipsum = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
    Nullam ultricies non leo semper fringilla. 
    Quisque metus sem, convallis quis lorem a, rutrum fermentum lorem. 
    Etiam egestas, nulla ut fermentum dignissim, felis lectus commodo mi, non lacinia ipsum enim id nisi. 
    Integer sed elementum nisl. 
    Pellentesque condimentum arcu lectus, ac hendrerit nulla viverra nec. Curabitur sit amet aliquam magna. 
    Proin a mattis dui."""

    def request_ipsum_sentencize(self) -> IpsumResponseModel:
        resp = requests.get("http://127.0.0.1/sentencize")
        resp.raise_for_status()  # fail fast if HTTP error

        # Validate JSON against the contract
        return IpsumResponseModel(**resp.json())


class Serve(unittest.TestCase):
    def test_serve_a_sentence_to_http_client(self):
        app = FastAPI()
        # TODO: vvv
        routes = MessageRoutes()
        app.include_router(routes.router)
        config = uvicorn.Config(app, host="127.0.0.1", port=80, log_level="warning")
        server = uvicorn.Server(config)

        thread = threading.Thread(target=server.run, daemon=True)
        thread.start()

        client = IpsumHttpClient()
        sentences = client.request_ipsum_sentencize().sentences

        self.assertTrue(len(sentences) > 0)
