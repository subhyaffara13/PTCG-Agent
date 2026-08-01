
def _i(c: bytes) -> int:
    return i32((b"\0\0\0\0" + c)[-4:])

