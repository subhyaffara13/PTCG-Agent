
def _to_list_of_ints(s: bytes) -> list[int]:
    s = s.replace(b',', b' ')
    return [_to_int(val) for val in s.split()]

