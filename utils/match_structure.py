
def match_structure(a: IntTuple, b: IntTuple) -> bool:
    if is_int(a) and is_int(b):
        return True
    if is_tuple(a) and is_tuple(b):
        return len(a) == len(b) and all(match_structure(x, y) for x, y in zip(a, b))
    return False

