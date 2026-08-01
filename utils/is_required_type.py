
def is_required_type(typ: type) -> bool:
    return get_origin(typ) == Required

