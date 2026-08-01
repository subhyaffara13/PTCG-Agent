
def from_string(value: str) -> "WrapModes":
    return getattr(WrapModes, str(value), None) or WrapModes(int(value))

