from typing import List, Tuple


def format_report(report_data: Tuple[List[Tuple[str, List[int]]], List[int], int]) -> str:
    rows, totals, total_requests = report_data
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    col_widths = [7, 7, 9, 7, 9]  # ширина под каждую колонку (подобрана под названия уровней)
    output = [f"Total requests: {total_requests}\n"]

    # Заголовок
    header = "HANDLER".ljust(22) + "".join(level.ljust(w) for level, w in zip(levels, col_widths))
    output.append(header)

    # Строки обработчиков
    for handler, counts in rows:
        row = handler.ljust(22) + "".join(str(count).ljust(w) for count, w in zip(counts, col_widths))
        output.append(row)

    # Строка total'ов
    totals_row = " " * 22 + "".join(str(total).ljust(w) for total, w in zip(totals, col_widths))
    output.append(totals_row)

    return "\n".join(output)
