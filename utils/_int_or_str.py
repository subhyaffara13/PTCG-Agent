from typing import Any

def _int_or_str(val: Any) -> Any:
    try:
        return int(val)
    except Exception:
        return val
