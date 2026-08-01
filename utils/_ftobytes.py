
def _ftobytes(f: float) -> bytes:
    return struct.Struct('f').pack(f)

