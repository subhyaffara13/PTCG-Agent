
def tagToIdentifier(tag: str | bytes) -> str:
    """Convert a table tag to a valid (but UGLY) python identifier,
    as well as a filename that's guaranteed to be unique even on a
    caseless file system. Each character is mapped to two characters.
    Lowercase letters get an underscore before the letter, uppercase
    letters get an underscore after the letter. Trailing spaces are
    trimmed. Illegal characters are escaped as two hex bytes. If the
    result starts with a number (as the result of a hex escape), an
    extra underscore is prepended. Examples:
    .. code-block:: pycon

        >>>
        >> tagToIdentifier('glyf')
        '_g_l_y_f'
        >> tagToIdentifier('cvt ')
        '_c_v_t'
        >> tagToIdentifier('OS/2')
        'O_S_2f_2'
    """
    import re

    tag = Tag(tag)
    if tag == "GlyphOrder":
        return tag
    assert len(tag) == 4, "tag should be 4 characters long"
    while len(tag) > 1 and tag[-1] == " ":
        tag = tag[:-1]
    ident = ""
    for c in tag:
        ident = ident + _escapechar(c)
    if re.match("[0-9]", ident):
        ident = "_" + ident
    return ident

