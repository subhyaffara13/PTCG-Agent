
def _get_u64(data: memoryview) -> tuple[int, memoryview]:
    """Uint64"""
    if len(data) < 8:
        raise ValueError("Invalid data")
    return int.from_bytes(data[:8], byteorder="big"), data[8:]

