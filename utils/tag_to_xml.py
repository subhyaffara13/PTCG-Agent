
def tagToXML(tag: str | bytes) -> str:
    """Similarly to tagToIdentifier(), this converts a TT tag
    to a valid XML element name. Since XML element names are
    case sensitive, this is a fairly simple/readable translation.
    """
    import re

    tag = Tag(tag)
    if tag == "OS/2":
        return "OS_2"
    elif tag == "GlyphOrder":
        return tag
    if re.match("[A-Za-z_][A-Za-z_0-9]* *$", tag):
        return tag.strip()
    else:
        return tagToIdentifier(tag)

