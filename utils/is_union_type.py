
def is_union_type(typ: type) -> bool:
    return _is_union(get_origin(typ))

