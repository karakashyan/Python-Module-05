from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        super().__init__()
        self._storage: list[tuple[int, str]] = []
        self._rank = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        ...

    def output(self) -> tuple[int, str]:
        return self._storage.pop(0)


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
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        items = data if isinstance(data, list) else [data]
        for i in items:
            self._storage.append((self._rank, str(i)))
            self._rank += 1


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
        if not self.validate(data):
            raise ValueError("Improper text data")
        items = data if isinstance(data, list) else [data]
        for i in items:
            self._storage.append((self._rank, i))
            self._rank += 1


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
        if not self.validate(data):
            raise ValueError("Improper log data")
        items = data if isinstance(data, list) else [data]
        for i in items:
            self._storage.append((self._rank, f"{': '.join(i.values())}"))
            self._rank += 1


if __name__ == "__main__":
    nump = NumericProcessor()
    print("=== Code Nexus - Data Processor ===")
    print()
    print("Testing Numeric Processor...")
    print(f"Trying to validate input '42': {nump.validate(42)}")
    print(f"Trying to validate input 'Hello': {nump.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        nump.ingest('foo')  # type: ignore[arg-type]
    except ValueError as e:
        print(f"Got exception: {e}")
    l1: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {l1}")
    nump.ingest(l1)
    print("Extracting 3 values...")
    for _ in range(3):
        x, y = nump.output()
        print(f"Numeric value {x}: {y}")
    print()

    tp = TextProcessor()
    print("Testing Text Processor...")
    print(f"Trying to validate input '42': {tp.validate(42)}")
    l2: list[str] = ['Hello', 'Nexus', 'World']
    print(f"Processing data: {l2}")
    tp.ingest(l2)
    print("Extracting 1 value...")
    x, y = tp.output()
    print(f"Text value {x}: {y}")
    print()

    lp = LogProcessor()
    print("Testing Log Processor...")
    print(f"Trying to validate input 'Hello': {lp.validate('Hello')}")
    l3: list[dict[str, str]] = [
            {'log_level': 'NOTICE', 'log_message': 'Connection to server'},
            {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}
         ]
    print(f"Processing data: {l3}")
    lp.ingest(l3)
    print("Extracting 2 values...")
    for _ in range(2):
        x, y = lp.output()
        print(f"Log entry {x}: {y}")
