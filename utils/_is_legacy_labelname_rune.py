
def _is_legacy_labelname_rune(b: str, i: int) -> bool:
    if len(b) != 1:
        raise ValueError("Input 'b' must be a single character.")
    return (
        ('a' <= b <= 'z')
        or ('A' <= b <= 'Z')
        or (b == '_')
        or ('0' <= b <= '9' and i > 0)
    )

