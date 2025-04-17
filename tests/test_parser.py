import pytest

from src.log_parser import parse_log_file


@pytest.fixture
def log_file(tmp_path):
    """Создание временного лог-файла с тестовыми данными."""
    content = (
        "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]\n"
        "2025-03-28 12:21:51,000 INFO django.request: GET /admin/dashboard/ 200 OK [192.168.1.68]\n"
        "2025-03-28 12:05:13,000 INFO django.request: GET /api/v1/reviews/ 201 OK [192.168.1.97]\n"
        "2025-03-28 12:11:57,000 ERROR django.request: Internal Server Error: /admin/dashboard/ [192.168.1.29]\n"
        "2025-03-28 12:40:47,000 CRITICAL django.core.management: DatabaseError: Deadlock detected\n"
    )
    log_file = tmp_path / "test.log"
    log_file.write_text(content)
    return log_file


def test_parse_log_file_valid(log_file):
    """Тест парсинга корректного лог-файла с несколькими обработчиками и уровнями логов."""
    result = parse_log_file(str(log_file))
    expected = {"/api/v1/reviews/": {"INFO": 2}, "/admin/dashboard/": {"INFO": 1, "ERROR": 1}}
    assert result == expected


def test_parse_log_file_empty(tmp_path):
    """Тест парсинга пустого лог-файла."""
    empty_file = tmp_path / "empty.log"
    empty_file.write_text("")
    result = parse_log_file(str(empty_file))
    assert result == {}


def test_parse_log_file_invalid_lines(tmp_path):
    """Тест парсинга файла, содержащего только некорректные строки."""
    content = (
        "2025-03-28 12:40:47,000 CRITICAL django.core.management: DatabaseError: Deadlock detected\n"
        "2025-03-28 12:25:45,000 DEBUG django.db.backends: (0.41) SELECT * FROM 'products'\n"
    )
    invalid_file = tmp_path / "invalid.log"
    invalid_file.write_text(content)
    result = parse_log_file(str(invalid_file))
    assert result == {}


def test_parse_log_file_large_file(tmp_path):
    """Тест парсинга большого лог-файла (эмуляция файла на гигабайты)."""
    content = (
        "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]\n"
        * 1000  # Симуляция множества строк
    )
    large_file = tmp_path / "large.log"
    large_file.write_text(content)
    result = parse_log_file(str(large_file))
    assert result == {"/api/v1/reviews/": {"INFO": 1000}}


def test_parse_log_file_mixed_methods(tmp_path):
    """Тест парсинга логов с методами GET и POST."""
    content = (
        "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]\n"
        "2025-03-28 12:44:47,000 INFO django.request: POST /api/v1/reviews/ 201 OK [192.168.1.60]\n"
    )
    mixed_file = tmp_path / "mixed.log"
    mixed_file.write_text(content)
    result = parse_log_file(str(mixed_file))
    assert result == {"/api/v1/reviews/": {"INFO": 2}}
