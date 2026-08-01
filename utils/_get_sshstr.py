
def _get_sshstr(data: memoryview) -> tuple[memoryview, memoryview]:
    """Bytes with u32 length prefix"""
    n, data = _get_u32(data)
    if n > len(data):
        raise ValueError("Invalid data")
    return data[:n], data[n:]

