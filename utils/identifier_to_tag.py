
def identifierToTag(ident: str) -> str:
    """the opposite of tagToIdentifier()"""
    if ident == "GlyphOrder":
        return ident
    if len(ident) % 2 and ident[0] == "_":
        ident = ident[1:]
    assert not (len(ident) % 2)
    tag = ""
    for i in range(0, len(ident), 2):
        if ident[i] == "_":
            tag = tag + ident[i + 1]
        elif ident[i + 1] == "_":
            tag = tag + ident[i]
        else:
            # assume hex
            tag = tag + chr(int(ident[i : i + 2], 16))
    # append trailing spaces
    tag = tag + (4 - len(tag)) * " "
    return Tag(tag)

