from src.ports.nlp.outbound.sentencizing import SentencizerPort


class Sentences:
    def __init__(self, sentencizer: SentencizerPort):
        self.sentencizer = sentencizer

    def break_apart(self, text: str) -> str:
        return self.sentencizer.get_sentences(text)
