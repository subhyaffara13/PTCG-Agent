from typing import Any

def has_members(cls: Any) -> bool:
    info = _resolve_opaque_type_info(cls)
    if info is None:
        return False
    return len(info.members) > 0

