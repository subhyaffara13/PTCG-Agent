
def sanitize_glyph_name(name):
    """Sanitize the glyph name to ensure it is valid according to FEA syntax."""
    sanitized = ""
    for i, c in enumerate(name):
        if i == 0 and c not in Lexer.CHAR_NAME_START_:
            sanitized += "a" + c
        elif c not in Lexer.CHAR_NAME_CONTINUATION_:
            sanitized += "_"
        else:
            sanitized += c

    return sanitized

