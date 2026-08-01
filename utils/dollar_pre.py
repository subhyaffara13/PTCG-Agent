
def dollar_pre(src: str, beg: int) -> bool:
    prv = charCodeAt(src[beg - 1], 0) if beg > 0 else False
    return (
        (not prv) or (prv != 0x5C and (prv < 0x30 or prv > 0x39))  # no backslash,
    )  # no decimal digit .. before opening '$'

