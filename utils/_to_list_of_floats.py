
def _to_list_of_floats(s: bytes | str) -> list[float]:
    return [_to_float(val) for val in s.split()]

