
def _escape_dn_value(val: str | bytes) -> str:
    """Escape special characters in RFC4514 Distinguished Name value."""

    if not val:
        return ""

    # RFC 4514 Section 2.4 defines the value as being the # (U+0023) character
    # followed by the hexadecimal encoding of the octets.
    if isinstance(val, bytes):
        return "#" + binascii.hexlify(val).decode("utf8")

    # See https://tools.ietf.org/html/rfc4514#section-2.4
    val = val.replace("\\", "\\\\")
    val = val.replace('"', '\\"')
    val = val.replace("+", "\\+")
    val = val.replace(",", "\\,")
    val = val.replace(";", "\\;")
    val = val.replace("<", "\\<")
    val = val.replace(">", "\\>")
    val = val.replace("\0", "\\00")

    if val[0] == "#" or (val[0] == " " and len(val) > 1):
        val = "\\" + val
    if val[-1] == " ":
        val = val[:-1] + "\\ "

    return val

