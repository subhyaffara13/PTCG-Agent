
def python_3000_invalid_escape_sequence(logical_line, tokens, noqa):
    r"""Invalid escape sequences are deprecated in Python 3.6.

    Okay: regex = r'\.png$'
    W605: regex = '\.png$'
    """
    if noqa:
        return

    # https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals
    valid = [
        '\n',
        '\\',
        '\'',
        '"',
        'a',
        'b',
        'f',
        'n',
        'r',
        't',
        'v',
        '0', '1', '2', '3', '4', '5', '6', '7',
        'x',

        # Escape sequences only recognized in string literals
        'N',
        'u',
        'U',
    ]

    prefixes = []
    for token_type, text, start, _, _ in tokens:
        if token_type in {tokenize.STRING, FSTRING_START, TSTRING_START}:
            # Extract string modifiers (e.g. u or r)
            prefixes.append(text[:text.index(text[-1])].lower())

        if token_type in {tokenize.STRING, FSTRING_MIDDLE, TSTRING_MIDDLE}:
            if 'r' not in prefixes[-1]:
                start_line, start_col = start
                pos = text.find('\\')
                while pos >= 0:
                    pos += 1
                    if text[pos] not in valid:
                        line = start_line + text.count('\n', 0, pos)
                        if line == start_line:
                            col = start_col + pos
                        else:
                            col = pos - text.rfind('\n', 0, pos) - 1
                        yield (
                            (line, col - 1),
                            f"W605 invalid escape sequence '\\{text[pos]}'"
                        )
                    pos = text.find('\\', pos + 1)

        if token_type in {tokenize.STRING, FSTRING_END, TSTRING_END}:
            prefixes.pop()

