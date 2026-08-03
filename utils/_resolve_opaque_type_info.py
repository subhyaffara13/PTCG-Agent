from typing import Any

def _resolve_opaque_type_info(cls: Any) -> _OpaqueTypeInfo | None:
    if cls in _OPAQUE_TYPES:
        return _OPAQUE_TYPES[cls]
    if not isinstance(cls, type):
        return None

    # Allow subclasses too
    for parent in cls.__mro__[1:]:
        if parent in _OPAQUE_TYPES:
            return _OPAQUE_TYPES[parent]
    return None

