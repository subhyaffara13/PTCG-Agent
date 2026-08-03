from typing import Any, Callable

def is_dynamo_disable_recursive(method: Callable[[Any], Any]) -> bool | None:
    """
    Check if a method is marked as `dynamo_disable` recursively. It returns:
    - True if disable(recursive=True)
    - False if disable(recursive=False)
    - None if method is not a disable decorator
    """
    return getattr(method, "_torchdynamo_disable_recursive", None)

