
def _uniToUnicode(component):
    """Helper for toUnicode() to handle "uniABCD" components."""
    match = _re_uni.match(component)
    if match is None:
        return None
    digits = match.group(1)
    if len(digits) % 4 != 0:
        return None
    chars = [int(digits[i : i + 4], 16) for i in range(0, len(digits), 4)]
    if any(c >= 0xD800 and c <= 0xDFFF for c in chars):
        # The AGL specification explicitly excluded surrogate pairs.
        return None
    return "".join([chr(c) for c in chars])

