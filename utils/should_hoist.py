
def should_hoist(cls: Any) -> bool:
    info = _resolve_opaque_type_info(cls)
    if info is None:
        return False
    return info.hoist

