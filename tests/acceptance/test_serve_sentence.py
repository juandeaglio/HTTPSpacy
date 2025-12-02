# tests/acceptance/test_server_sentence.py
import unittest
import requests

from pydantic import BaseModel
from typing import List

from src.adapters.web.app import create_app
from src.adapters.web.server import create_server



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
        app = create_app()
        server = create_server(app, "127.0.0.1", 80)
        server.start()

        client = IpsumHttpClient()
        sentences = client.request_ipsum_sentencize().sentences

        self.assertTrue(len(sentences) > 0)
