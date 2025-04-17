import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import List

from src.log_parser import parse_log_file
from src.reports.handlers import HandlersReport


def main() -> None:
    parser = argparse.ArgumentParser(description="Django log analyzer")
    parser.add_argument("log_files", nargs="+", help="Paths to log files")
    parser.add_argument("--report", default="handlers", help="Report type")
    args = parser.parse_args()

    # Проверка файлов
    log_files: List[str] = args.log_files
    for log_file in log_files:
        if not os.path.exists(log_file):
            print(f"Error: File {log_file} does not exist", file=sys.stderr)
            sys.exit(1)

    # Проверка отчёта
    if args.report != "handlers":
        print("Error: Invalid report name. Only 'handlers' is supported", file=sys.stderr)
        sys.exit(1)

    # Параллельная обработка
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(parse_log_file, log_files))

    # Объединение результатов
    combined_stats = {}
    for result in results:
        for handler, levels in result.items():
            if handler not in combined_stats:
                combined_stats[handler] = {}
            for level, count in levels.items():
                combined_stats[handler][level] = combined_stats[handler].get(level, 0) + count

    # Генерация и вывод отчёта
    report = HandlersReport()
    output = report.generate(data=combined_stats)
    print(output)


if __name__ == "__main__":
    main()
