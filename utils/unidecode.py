
def unidecode(txt):
    chars = []
    for ch in txt:
        codepoint = ord(ch)

        if not codepoint:
            chars.append('\x00')
            continue

        try:
            chars.append(_replaces[codepoint-1])
        except IndexError:
            pass
    return "".join(chars)

