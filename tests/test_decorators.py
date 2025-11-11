# tests/test_log_decorator.py
import re

import pytest

from src.decorators import log


@log
def add(a, b):
    """Sum two numbers (for console tests)."""
    return a + b


@log
def boom(x):
    """Raise ZeroDivisionError when x == 0 (for console tests)."""
    return 10 / x


def test_log_console_success(capsys):
    res = add(2, 3)
    assert res == 5

    out = capsys.readouterr().out
    # Должны увидеть CALL и RETURN
    assert re.search(r"\[.*\]\s+CALL\s+add\(\s*2,\s*3\s*\)", out)
    assert re.search(r"\[.*\]\s+RETURN\s+add\s+->\s+5\b", out)


def test_log_console_exception(capsys):
    with pytest.raises(ZeroDivisionError):
        boom(0)

    out = capsys.readouterr().out
    # Должны увидеть CALL, затем ERROR с типом исключения и traceback
    assert re.search(r"\[.*\]\s+CALL\s+boom\(\s*0\s*\)", out)
    assert re.search(r"ERROR\s+boom", out)
    assert "ZeroDivisionError" in out
    assert "Traceback (most recent call last)" in out


def test_log_file_success_and_kwargs(tmp_path):
    logfile = tmp_path / "app.log"

    @log(filename=str(logfile))
    def mix(a, b, z=0):
        """Return a + b + z and log to file."""
        return a + b + z

    # Первый вызов с kwargs
    r1 = mix(2, 3, z=4)
    # Второй вызов без kwargs (протестируем дописывание в файл)
    r2 = mix(1, 2)

    assert r1 == 9
    assert r2 == 3

    text = logfile.read_text(encoding="utf-8")
    # Есть две записи CALL и две RETURN
    assert text.count("CALL") >= 2
    assert text.count("RETURN") >= 2

    # Проверим строку с аргументами и возвратами
    assert "mix(2, 3, z=4)" in text
    assert re.search(r"RETURN\s+mix\s+->\s+9\b", text)
    assert re.search(r"RETURN\s+mix\s+->\s+3\b", text)


def test_log_file_exception(tmp_path):
    logfile = tmp_path / "errors.log"

    @log(filename=str(logfile))
    def fail(msg):
        raise ValueError(f"bad: {msg}")

    with pytest.raises(ValueError):
        fail("boom")

    text = logfile.read_text(encoding="utf-8")
    # Есть CALL, потом ERROR, тип и traceback
    assert re.search(r"\[.*\]\s+CALL\s+fail\(", text)
    assert re.search(r"ERROR\s+fail", text)
    assert "ValueError: bad: boom" in text
    assert "Traceback (most recent call last)" in text
    # В ERROR-строке должны быть args=(
    assert "args=(" in text


def test_wraps_preserved():
    assert add.__name__ == "add"
    assert "Sum two numbers" in (add.__doc__ or "")
    assert boom.__name__ == "boom"
    assert "ZeroDivisionError" in (boom.__doc__ or "")
