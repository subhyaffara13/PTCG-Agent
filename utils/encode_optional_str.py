
def encode_optional_str(s: str | None) -> str:
    if s is None:
        return "<None>"
    else:
        return s

