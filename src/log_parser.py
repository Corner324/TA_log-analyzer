import re
from collections import defaultdict
from typing import Dict

LOG_PATTERN = re.compile(
    r"(DEBUG|INFO|WARNING|ERROR|CRITICAL) django\.request: (?:(GET|POST) (\S+?) \d{3} OK|Internal Server Error: (\S+))"
)


def parse_log_file(file_path: str) -> Dict[str, Dict[str, int]]:
    stats = defaultdict(lambda: defaultdict(int))
    with open(file_path, "r", buffering=1) as f:
        for line in f:
            match = LOG_PATTERN.search(line)
            if match:
                level, method, handler_get_post, handler_error = match.groups()
                handler = handler_get_post or handler_error
                stats[handler][level] += 1
    return dict(stats)
