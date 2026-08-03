from typing import Any

def _is_list_of_str(obj: Any) -> bool:
    return isinstance(obj, list) and all(isinstance(item, str) for item in obj)

