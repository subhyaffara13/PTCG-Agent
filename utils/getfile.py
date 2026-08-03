from typing import Any

def getfile(obj: Any) -> str | None:
    try:
        return inspect.getfile(obj)
    except (TypeError, OSError):
        return None

