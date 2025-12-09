from typing import List

from src.ports.nlp.outbound.sentencizing import SentencizerPort


class SpacySentencizer(SentencizerPort):
    def get_sentences(self, text: str) -> List[str]:
        pass

