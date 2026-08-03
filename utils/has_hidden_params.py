from typing import Any

def has_hidden_params(obj: Any) -> bool:
    return hasattr(obj, "_hidden_params")

