from abc import ABC, abstractmethod
from typing import List


class SentencizerPort(ABC):
    @abstractmethod
    def get_sentences(self, text: str) -> List[str]:
        pass
