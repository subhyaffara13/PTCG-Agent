
def nextheader(fobj: IO[bytes]) -> tuple[bytes, int]:
    return struct.unpack(">4sI", fobj.read(HEADERSIZE))

