
def _check_byteslike(name: str, value: Buffer) -> None:
    try:
        memoryview(value)
    except TypeError:
        raise TypeError(f"{name} must be bytes-like")

