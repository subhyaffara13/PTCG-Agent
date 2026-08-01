
def _get_all_tokens(line, lines):
    '''Starting from *line*, generate the necessary tokens which represent the
    shortest tokenization possible. This is done by catching
    :exc:`tokenize.TokenError` when a multi-line string or statement is
    encountered.
    :returns: tokens, lines
    '''
    buffer = line
    used_lines = [line]
    while True:
        try:
            tokens = _generate(buffer)
        except tokenize.TokenError:
            # A multi-line string or statement has been encountered:
            # start adding lines and stop when tokenize stops complaining
            pass
        else:
            if not any(t[0] == tokenize.ERRORTOKEN for t in tokens):
                return tokens, used_lines

        # Add another line
        next_line = next(lines)
        buffer = buffer + '\n' + next_line
        used_lines.append(next_line)

