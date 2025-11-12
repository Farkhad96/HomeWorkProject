import traceback
from datetime import datetime
from functools import wraps


def log(_func=None, *, filename=None):
    """
    Декоратор для логирования вызовов функций, их возвратов и исключений.
    Логи пишутся в консоль или в указанный файл.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def _write(line: str):
                if filename is None:
                    print(line)
                else:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(line + "\n")

            # Время вызова и аргументы
            called_at = datetime.now()
            args_str = ", ".join([*(repr(a) for a in args), *(f"{k}={v!r}" for k, v in kwargs.items())])
            _write(f"[{called_at:%Y-%m-%d %H:%M:%S}] CALL   {func.__name__}({args_str})")
            start = called_at
            try:
                result = func(*args, **kwargs)
                elapsed_ms = (datetime.now() - start).total_seconds() * 1000
                _write(
                    f"[{datetime.now():%Y-%m-%d %H:%M:%S}] RETURN {func.__name__} -> {result!r} "
                    f"(elapsed {elapsed_ms:.2f} ms)"
                )
                return result
            except Exception as e:
                elapsed_ms = (datetime.now() - start).total_seconds() * 1000
                _write(
                    f"[{datetime.now():%Y-%m-%d %H:%M:%S}] ERROR  {func.__name__}: "
                    f"{type(e).__name__}: {e} | args=({args_str}) "
                    f"(elapsed {elapsed_ms:.2f} ms)"
                )
                _write("".join(traceback.format_exc()).rstrip())
                raise

        return wrapper

    if _func is None:
        return decorator
    return decorator(_func)
