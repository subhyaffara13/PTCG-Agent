from typing import Any

def is_torch_function_object(value: Any) -> bool:
    return hasattr(value, "__torch_function__")

