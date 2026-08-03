from typing import Any, Callable

def naturally(
    to_sort: Iterable[str], key: Callable[[str], Any] | None = None, reverse: bool = False
) -> list[str]:
    """Returns a naturally sorted list"""
    if key is None:
        key_callback = _natural_keys
    else:

        def key_callback(text: str) -> list[Any]:
            return _natural_keys(key(text))

    return sorted(to_sort, key=key_callback, reverse=reverse)

