from typing import Any

def is_aot(obj: Any) -> bool:
    """Decides if an object behaves as an array of tables (i.e. a nonempty list
    of dicts)."""
    return bool(
        isinstance(obj, ARRAY_TYPES)
        and obj
        and all(isinstance(v, Mapping) for v in obj)
    )


def is_aot(obj: Any) -> bool:
    """Decides if an object behaves as an array of tables (i.e. a nonempty list
    of dicts)."""
    return bool(
        isinstance(obj, ARRAY_TYPES)
        and obj
        and all(isinstance(v, Mapping) for v in obj)
    )

