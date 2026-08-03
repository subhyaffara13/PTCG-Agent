from typing import Any

def _builtin_exceptions() -> set[str]:
    def predicate(obj: Any) -> bool:
        return isinstance(obj, type) and issubclass(obj, BaseException)

    members = inspect.getmembers(builtins, predicate)
    return {exc.__name__ for (_, exc) in members}

