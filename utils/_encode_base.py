
def _encode_base(digits: Sequence[int], base: int) -> int:
    value = 0
    for d in digits:
        value = value * base + int(d)
    return value

