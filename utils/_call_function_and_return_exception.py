from typing import Any, Callable

def _call_function_and_return_exception(
    func: Callable[[Unpack[_Ts]], _R], args: tuple[Unpack[_Ts]], kwargs: dict[str, Any]
) -> _R | Exception:
    """Call function and return a exception if there is one."""

    try:
        return func(*args, **kwargs)
    except Exception as e:
        return e

