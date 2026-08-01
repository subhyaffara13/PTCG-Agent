
def check_opaque_obj(value: Any, metadata: Any) -> bool:
    if metadata is None:
        return True
    opaque_info = get_opaque_obj_info(type(value))
    if not opaque_info or not opaque_info.guard_fn:
        return metadata is None
    return opaque_info.guard_fn(value) == metadata

