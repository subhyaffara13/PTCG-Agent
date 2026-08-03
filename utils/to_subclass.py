from typing import Any

def to_subclass(t: Any, cls: type) -> Any:
    return t.as_subclass(cls)

