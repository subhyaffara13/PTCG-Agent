
def _unescape_dn_value(val: str) -> str:
    if not val:
        return ""

    # See https://tools.ietf.org/html/rfc4514#section-3

    # special = escaped / SPACE / SHARP / EQUALS
    # escaped = DQUOTE / PLUS / COMMA / SEMI / LANGLE / RANGLE
    def sub(m):
        val = m.group(0)
        # Special character escape
        if len(val) == 2:
            return val[1:]

        # Unicode string of hex
        return binascii.unhexlify(val.replace("\\", "")).decode()

    return _RFC4514NameParser._PAIR_MULTI_RE.sub(sub, val)

