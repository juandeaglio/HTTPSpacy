from abc import ABC, abstractmethod


class SentencizerPort(ABC):
    @abstractmethod
    def get_sentences(self, text: str) -> str:
        pass
