from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        super().__init__()
        self._storage = []
        self._rank = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        ...

    def output(self) -> tuple[int, str]:
        ...


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        if isinstance(data, list):
            return all(
                isinstance(i, (int, float)) and not isinstance(i, bool)
                for i in data
            )
        return False


    def ingest(self, data: int | float | list[int | float]) -> None:
        DataProcessor._storage(DataProcessor._rank, data)


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(
                isinstance(i, str)
                for i in data
            )
        return False

    def ingest(self, data: str | list[str]) -> None:
        ...

class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            for key, value in data.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    return False
            return True
        if isinstance(data, list):
            return all(
                isinstance(i, dict) and
                all(
                    isinstance(key, str) and isinstance(value, str)
                    for key, value in i.items()
                )
                for i in data
            )
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        ...

if __name__ == "__main__":
