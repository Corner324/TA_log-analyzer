from abc import ABC, abstractmethod
from typing import Any, Dict


class Report(ABC):
    @abstractmethod
    def generate(self, data: Dict[str, Dict[str, int]]) -> Any:
        pass
