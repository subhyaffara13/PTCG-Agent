
def create_valid_python_identifier(name: str) -> str:
    """
    Create valid Python identifiers from any string.

    Check if name contains any special characters. If it contains any
    special characters, the special characters will be replaced by
    a special string and a prefix is added.

    Raises
    ------
    SyntaxError
        If the returned name is not a Python valid identifier, raise an exception.
    """
    if name.isidentifier() and not iskeyword(name):
        return name

    # Escape characters that fall outside the ASCII range (U+0001..U+007F).
    # GH 49633
    gen = (
        (c, "".join(chr(b) for b in c.encode("ascii", "backslashreplace")))
        for c in name
    )
    name = "".join(
        c_escaped.replace("\\", "_UNICODE_" if c != c_escaped else "_BACKSLASH_")
        for c, c_escaped in gen
    )

    # Create a dict with the special characters and their replacement string.
    # EXACT_TOKEN_TYPES contains these special characters
    # token.tok_name contains a readable description of the replacement string.
    special_characters_replacements = {
        char: f"_{token.tok_name[tokval]}_"
        for char, tokval in (tokenize.EXACT_TOKEN_TYPES.items())
    }
    special_characters_replacements.update(
        {
            " ": "_",
            "?": "_QUESTIONMARK_",
            "!": "_EXCLAMATIONMARK_",
            "$": "_DOLLARSIGN_",
            "€": "_EUROSIGN_",
            "°": "_DEGREESIGN_",
            "'": "_SINGLEQUOTE_",
            '"': "_DOUBLEQUOTE_",
            "#": "_HASH_",
            "`": "_BACKTICK_",
        }
    )

    name = "".join([special_characters_replacements.get(char, char) for char in name])
    name = f"BACKTICK_QUOTED_STRING_{name}"

    if not name.isidentifier():
        raise SyntaxError(f"Could not convert '{name}' to a valid Python identifier.")

    return name

