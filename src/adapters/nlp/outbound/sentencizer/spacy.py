from typing import List

from src.ports.nlp.outbound.sentencizing import SentencizerPort
from spacy.pipeline.sentencizer import Sentencizer
from spacy.lang.en import English


class SpacySentencizer(SentencizerPort):
    def get_sentences(self, text: str) -> List[str]:
        nlp = English()
        nlp.add_pipe("sentencizer")
        sentence_spans = nlp(text).sents

        sentences = [sent.text for sent in sentence_spans]

        return sentences
