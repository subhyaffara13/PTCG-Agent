
def _raw_hex_id(obj) -> str:
    """Return the padded hexadecimal id of ``obj``."""
    # interpret as a pointer since that's what really what id returns
    packed = struct.pack("@P", id(obj))
    return "".join([_replacer(x) for x in packed])

