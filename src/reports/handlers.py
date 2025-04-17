from typing import Dict, List, Tuple

from src.formatter import format_report


class HandlersReport:
    def generate(self, data: Dict[str, Dict[str, int]]) -> str:
        rows: List[Tuple[str, List[int]]] = []
        levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        total_requests = 0
        totals = [0] * len(levels)

        for handler, handler_stats in sorted(data.items()):
            counts = [handler_stats.get(level, 0) for level in levels]
            rows.append((handler, counts))
            for i, count in enumerate(counts):
                totals[i] += count
            total_requests += sum(counts)

        return format_report((rows, totals, total_requests))
