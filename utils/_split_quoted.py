
def _split_quoted(text, separator, maxsplit=0):
    """Splits on split_ch similarly to strings.split, skipping separators if
    they are inside quotes.
    """

    tokens = ['']
    x = 0
    while x < len(text):
        split_pos = _next_unquoted_char(text, separator, x)
        if split_pos == -1:
            tokens[-1] = text[x:]
            x = len(text)
            continue
        # If the first character is the separator keep going. This happens when
        # there are double whitespace characters separating symbols.
        if split_pos == x:
            x += 1
            continue

        if maxsplit > 0 and len(tokens) > maxsplit:
            tokens[-1] = text[x:]
            break
        tokens[-1] = text[x:split_pos]
        x = split_pos + 1
        tokens.append('')
    return tokens

