
def bytes_to_int(bytestr: bytes) -> int:
    return _bytes_to_int(bytestr.rjust(8, b"\x00"))[0]

