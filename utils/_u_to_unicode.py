
def _uToUnicode(component):
    """Helper for toUnicode() to handle "u1ABCD" components."""
    match = _re_u.match(component)
    if match is None:
        return None
    digits = match.group(1)
    try:
        value = int(digits, 16)
    except ValueError:
        return None
    if (value >= 0x0000 and value <= 0xD7FF) or (value >= 0xE000 and value <= 0x10FFFF):
        return chr(value)
    return None

