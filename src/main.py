import argparse
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List


def main() -> None:
    parser = argparse.ArgumentParser(description="Django log analyzer")
    parser.add_argument("log_files", nargs="+", help="Paths to log files")
    parser.add_argument("--report", default="handlers", help="Report type")
    args = parser.parse_args()

    # Проверка файлов
    log_files: List[str] = args.log_files
    for log_file in log_files:
        if not os.path.exists(log_file):
            raise FileNotFoundError(f"File {log_file} does not exist")

    # Проверка отчёта
    if args.report != "handlers":
        raise ValueError("Only 'handlers' report is supported")

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
    output = report.generate(combined_stats)
    print(format_report(output))


if __name__ == "__main__":
    main()
