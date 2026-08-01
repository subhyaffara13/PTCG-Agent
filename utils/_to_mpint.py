
def _to_mpint(val: int) -> bytes:
    """Storage format for signed bigint."""
    if val < 0:
        raise ValueError("negative mpint not allowed")
    if not val:
        return b""
    nbytes = (val.bit_length() + 8) // 8
    return utils.int_to_bytes(val, nbytes)

