
def int_to_bytes(integer: int, length: int | None = None) -> bytes:
    if length == 0:
        raise ValueError("length argument can't be 0")
    return integer.to_bytes(
        length or (integer.bit_length() + 7) // 8 or 1, "big"
    )


def int_to_bytes(num: int) -> bytes:
    return _int_to_bytes(num).lstrip(b"\x00")

