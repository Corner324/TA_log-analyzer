from typing import Dict, List, Tuple

from .base import Report


class HandlersReport(Report):
    LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    def generate(self, data: Dict[str, Dict[str, int]]) -> Tuple[List[Tuple[str, List[int]]], List[int], int]:
        handlers = sorted(data.keys())
        rows = []
        totals = [0] * len(self.LEVELS)
        total_requests = 0

        for handler in handlers:
            counts = [data[handler].get(level, 0) for level in self.LEVELS]
            rows.append((handler, counts))
            for i, count in enumerate(counts):
                totals[i] += count
            total_requests += sum(counts)

        return rows, totals, total_requests
