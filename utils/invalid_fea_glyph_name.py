
def invalid_fea_glyph_name(name):
    """Check if the glyph name is valid according to FEA syntax."""
    if name[0] not in Lexer.CHAR_NAME_START_:
        return True
    if any(c not in Lexer.CHAR_NAME_CONTINUATION_ for c in name[1:]):
        return True
    return False

