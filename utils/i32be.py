
def i32be(c: bytes, o: int = 0) -> int:
    return unpack_from(">I", c, o)[0]

