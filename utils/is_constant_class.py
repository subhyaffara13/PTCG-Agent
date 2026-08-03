from typing import Any

def is_constant_class(cls: type[Any]) -> bool:
    return isinstance(cls, type) and cls in CONSTANT_NODES

