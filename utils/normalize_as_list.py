from typing import Any

def normalize_as_list(x: Any) -> list[Any]:
    if isinstance(x, tuple):
        return list(x)
    elif isinstance(x, list):
        return x
    return [x]


def normalize_as_list(x: _T) -> list[_T]: ...


def normalize_as_list(x: tuple[_T, ...]) -> list[_T]: ...


def normalize_as_list(x: list[_T]) -> list[_T]: ...


def normalize_as_list(x: object) -> list[object]:
    if isinstance(x, tuple):
        return list(x)
    elif isinstance(x, list):
        return x
    return [x]

