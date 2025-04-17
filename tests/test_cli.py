import sys
from unittest.mock import patch

import pytest

from src.formatter import format_report
from src.main import main
from src.reports.handlers import HandlersReport


def test_main_no_arguments(capsys):
    """Тест: если не переданы аргументы, main завершается с ошибкой."""
    with pytest.raises(SystemExit) as exc_info:
        sys.argv = ["main.py"]
        main()
    assert exc_info.value.code == 2  # Код ошибки argparse
    captured = capsys.readouterr()
    assert "error: the following arguments are required" in captured.err


def test_main_nonexistent_file(capsys):
    """Тест обработки ошибки при отсутствии лог-файла."""
    with pytest.raises(SystemExit) as exc_info:
        sys.argv = ["main.py", "nonexistent.log", "--report", "handlers"]
        main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error: File nonexistent.log does not exist" in captured.err


def test_main_invalid_report(tmp_path, capsys):
    """Тест обработки ошибки при неверном имени отчёта."""
    log_file = tmp_path / "test.log"
    log_file.write_text("")  # Создаём пустой файл
    with pytest.raises(SystemExit) as exc_info:
        sys.argv = ["main.py", str(log_file), "--report", "invalid"]
        main()
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "Error: Invalid report name. Only 'handlers' is supported" in captured.err


def test_main_valid_arguments(tmp_path, capsys):
    """Тест main с корректными аргументами и проверкой вывода отчёта."""
    log_content = (
        "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK\n"
        "2025-03-28 12:11:57,000 ERROR django.request: Internal Server Error: /admin/dashboard/\n"
    )
    log_file = tmp_path / "test.log"
    log_file.write_text(log_content)

    # Создаём ожидаемый результат для мока
    stats = {"/api/v1/reviews/": {"INFO": 1}, "/admin/dashboard/": {"ERROR": 1}}
    rows = [("/admin/dashboard/", [0, 0, 0, 1, 0]), ("/api/v1/reviews/", [0, 1, 0, 0, 0])]
    totals = [0, 1, 0, 1, 0]
    total_requests = 2
    expected_output = format_report((rows, totals, total_requests))

    sys.argv = ["main.py", str(log_file), "--report", "handlers"]
    with patch.object(HandlersReport, "generate", return_value=expected_output) as mock_generate:
        main()
        mock_generate.assert_called_once_with(data=stats)

    captured = capsys.readouterr()
    assert "Total requests: 2" in captured.out
    assert "/api/v1/reviews/" in captured.out
    assert "/admin/dashboard/" in captured.out
    assert "INFO" in captured.out
    assert "ERROR" in captured.out


def test_main_multiple_files(tmp_path, capsys):
    """Тест main при передаче нескольких лог-файлов."""
    log_content1 = "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK\n"
    log_content2 = "2025-03-28 12:11:57,000 ERROR django.request: Internal Server Error: /admin/dashboard/\n"
    log_file1 = tmp_path / "test1.log"
    log_file2 = tmp_path / "test2.log"
    log_file1.write_text(log_content1)
    log_file2.write_text(log_content2)

    sys.argv = ["main.py", str(log_file1), str(log_file2), "--report", "handlers"]
    main()

    captured = capsys.readouterr()
    assert "Total requests: 2" in captured.out
    assert "/api/v1/reviews/" in captured.out
    assert "/admin/dashboard/" in captured.out
