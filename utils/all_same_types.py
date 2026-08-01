
def all_same_types(types: list[Type]) -> bool:
    if not types:
        return True
    return all(is_same_type(t, types[0]) for t in types[1:])

