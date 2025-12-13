# tests/acceptance/test_server_sentence.py
import unittest
import requests

from pydantic import BaseModel
from typing import List
from tests.examples import sample_text


class IpsumResponseModel(BaseModel):
    sentences: List[str]


class IpsumHttpClient:
    ipsum = sample_text

    def request_ipsum_sentencize(self) -> IpsumResponseModel:
        resp = requests.post("http://127.0.0.1:8980/sentencize", json={"body": self.ipsum})
        resp.raise_for_status()  # fail fast if HTTP error

        # Validate JSON against the contract
        return IpsumResponseModel(**resp.json())


class ServeTestCase(unittest.TestCase):
    def test_serve_a_sentence_to_http_client(self):
        client = IpsumHttpClient()
        sentences = client.request_ipsum_sentencize().sentences

        self.assertTrue(len(sentences) > 0)
