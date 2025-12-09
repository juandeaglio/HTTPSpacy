import unittest
from unittest.mock import Mock

from src.application.sentences import Sentences
from tests.examples import sample_text
from src.ports.nlp.outbound.sentencizing import SentencizerPort


class SentencesPort(unittest.TestCase):
    def test_sentencize(self):
        mocked_adapter = Mock(SentencizerPort)
        Sentences(mocked_adapter).break_apart(sample_text)
        mocked_adapter.get_sentences.assert_called()
