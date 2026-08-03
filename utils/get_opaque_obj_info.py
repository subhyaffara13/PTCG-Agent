from typing import Any

def get_opaque_obj_info(cls: Any) -> _OpaqueTypeInfo | None:
    if not is_opaque_type(cls):
        return None

    if isinstance(cls, str):
        return _OPAQUE_TYPES_BY_NAME[cls]

    return _resolve_opaque_type_info(cls)

