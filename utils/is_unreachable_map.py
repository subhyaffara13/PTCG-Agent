
def is_unreachable_map(map: TypeMap) -> bool:
    return any(isinstance(get_proper_type(v), UninhabitedType) for v in map.values())

