from typing import Any

def extract_opaque_obj(guard: Any, value: Any) -> Any:
    opaque_info = get_opaque_obj_info(type(value))
    if not opaque_info or not opaque_info.guard_fn:
        return None
    return deepcopy(opaque_info.guard_fn(value))

