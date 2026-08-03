from typing import Any

def is_async_iterable(obj: Any) -> bool:
    """
    Check if an object is an async iterable (can be used with 'async for').

    Args:
        obj: Any Python object to check

    Returns:
        bool: True if the object is async iterable, False otherwise
    """
    return isinstance(obj, collections.abc.AsyncIterable)

