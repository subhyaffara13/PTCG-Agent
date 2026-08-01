
def _get_mpint(data: memoryview) -> tuple[int, memoryview]:
    """Big integer."""
    val, data = _get_sshstr(data)
    if val and val[0] > 0x7F:
        raise ValueError("Invalid data")
    return int.from_bytes(val, "big"), data

