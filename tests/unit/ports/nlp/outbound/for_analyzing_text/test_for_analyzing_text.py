import unittest

from src.adapters.nlp.outbound.sentencizer.stub import StubSentencizer
from tests.examples import sample_text


class AnalyzingTestCase(unittest.TestCase):
    def test_analyze_text(self):
        split_sentences = StubSentencizer().get_sentences(sample_text)
        self.assertEqual(len(split_sentences), 8, "Sentences were not split correctly.")


if __name__ == '__main__':
    unittest.main()
