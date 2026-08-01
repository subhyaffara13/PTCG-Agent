
def _get_u32(data: memoryview) -> tuple[int, memoryview]:
    """Uint32"""
    if len(data) < 4:
        raise ValueError("Invalid data")
    return int.from_bytes(data[:4], byteorder="big"), data[4:]

