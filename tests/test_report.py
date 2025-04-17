from src.reports.handlers import HandlersReport


def test_handlers_report_empty():
    """Тест на генерацию отчёта HandlersReport при пустой статистике."""
    stats = {}
    report = HandlersReport()
    result = report.generate(data=stats)

    expected = (
        "Total requests: 0\n\n"
        "HANDLER               DEBUG  INFO   WARNING  ERROR  CRITICAL \n"
        "                      0      0      0        0      0        "
    )
    assert result == expected


def test_handlers_report_formatting():
    """Тест на форматирование таблицы отчёта."""
    stats = {"/api/v1/reviews/": {"INFO": 1}}
    report = HandlersReport()
    result = report.generate(data=stats)
    lines = result.splitlines()
    assert lines[0] == "Total requests: 1"
    assert lines[2] == "HANDLER               DEBUG  INFO   WARNING  ERROR  CRITICAL "
    assert lines[3].startswith("/api/v1/reviews/")
    assert "1" in lines[3]  # Счётчик INFO


def test_handlers_report_single_handler():
    """Тест отчёта HandlersReport с одним обработчиком."""
    stats = {"/api/v1/reviews/": {"INFO": 2, "ERROR": 1}}
    report = HandlersReport()
    result = report.generate(data=stats)
    assert "Total requests: 3" in result
    assert "/api/v1/reviews/" in result
    assert "2" in result  # Счётчик INFO
    assert "1" in result  # Счётчик ERROR
    assert "0" in result  # DEBUG, WARNING, CRITICAL


def test_handlers_report_multiple_handlers():
    """Тест отчёта HandlersReport с несколькими обработчиками и уровнями логирования."""
    stats = {"/api/v1/reviews/": {"INFO": 2, "ERROR": 1}, "/admin/dashboard/": {"INFO": 1, "DEBUG": 1, "CRITICAL": 1}}
    report = HandlersReport()
    result = report.generate(data=stats)
    assert "Total requests: 6" in result
    assert "/api/v1/reviews/" in result
    assert "/admin/dashboard/" in result
    assert "2" in result  # INFO для reviews
    assert "1" in result  # ERROR для reviews
    assert "1" in result  # DEBUG для dashboard


def test_handlers_report_all_levels():
    """Тест HandlersReport с полным набором уровней логирования."""
    stats = {"/api/v1/reviews/": {"DEBUG": 1, "INFO": 1, "WARNING": 1, "ERROR": 1, "CRITICAL": 1}}
    report = HandlersReport()
    result = report.generate(data=stats)
    assert "Total requests: 5" in result
    assert "1" in result  # По одному для каждого уровня
