
def _read_unpacked(f: IO[bytes], fmt: str) -> Tuple[int, ...]:
    return struct.unpack(fmt, f.read(struct.calcsize(fmt)))

