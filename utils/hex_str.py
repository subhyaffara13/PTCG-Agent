
def hexStr(data):
    """Convert binary data to a hex string."""
    h = string.hexdigits
    r = ""
    for c in data:
        i = byteord(c)
        r = r + h[(i >> 4) & 0xF] + h[i & 0xF]
    return r


def hexStr(s):
    h = string.hexdigits
    r = ""
    for c in s:
        i = byteord(c)
        r = r + h[(i >> 4) & 0xF] + h[i & 0xF]
    return r

