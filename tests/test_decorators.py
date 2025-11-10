# test_decorators.py
import pytest
from src.decorators import log


# Пример функций для тестирования
@log()
def successful_function(x, y):
    return x + y


@log()
def error_function(x, y):
    return x / y  # Может вызвать ошибку деления на ноль


def test_successful_function(capsys):
    # Тестируем успешное выполнение
    result = successful_function(10, 5)
    assert result == 15

    # Перехватываем вывод
    captured = capsys.readouterr()

    # Проверяем, что вывод содержит информацию о выполнении
    assert "Начало выполнения функции 'successful_function'" in captured.out
    assert "Функция 'successful_function' завершена успешно." in captured.out
    assert "Время выполнения функции 'successful_function'" in captured.out


def test_error_function(capsys):
    # Тестируем функцию с ошибкой
    with pytest.raises(ZeroDivisionError):
        error_function(10, 0)

    # Перехватываем вывод
    captured = capsys.readouterr()

    # Проверяем, что вывод содержит информацию об ошибке
    assert "Начало выполнения функции 'error_function'" in captured.out
    assert "Ошибка в функции 'error_function': ZeroDivisionError" in captured.out
