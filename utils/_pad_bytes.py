
def _pad_bytes(name: AnyStr, length: int) -> AnyStr:
    """
    Take a char string and pads it with null bytes until it's length chars.
    """
    if isinstance(name, bytes):
        return name + b"\x00" * (length - len(name))
    return name + "\x00" * (length - len(name))

