
def i16be(c: bytes, o: int = 0) -> int:
    return unpack_from(">H", c, o)[0]

