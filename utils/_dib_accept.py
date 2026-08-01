
def _dib_accept(prefix: bytes) -> bool:
    return i32(prefix) in [12, 40, 52, 56, 64, 108, 124]

