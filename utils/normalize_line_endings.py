
def normalize_line_endings(value: bytes) -> bytes:
    return value.replace(os.linesep.encode("utf-8"), b"\n")

