from typing import List, Tuple


def format_report(report_data: Tuple[List[Tuple[str, List[int]]], List[int], int]) -> str:
    rows, totals, total_requests = report_data
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    output = [f"Total requests: {total_requests}\n"]
    output.append(f"{'HANDLER': <22} {'  '.join(f'{level: <8}' for level in levels)}")

    for handler, counts in rows:
        output.append(f"{handler: <22} {'  '.join(f'{count: <8}' for count in counts)}")

    output.append(f"{'': <22} {'  '.join(f'{total: <8}' for total in totals)}")
    return "\n".join(output)
