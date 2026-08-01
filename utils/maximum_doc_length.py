
def maximum_doc_length(logical_line, max_doc_length, noqa, tokens):
    r"""Limit all doc lines to a maximum of 72 characters.

    For flowing long blocks of text (docstrings or comments), limiting
    the length to 72 characters is recommended.

    Reports warning W505
    """
    if max_doc_length is None or noqa:
        return

    prev_token = None
    skip_lines = set()
    # Skip lines that
    for token_type, text, start, end, line in tokens:
        if token_type not in SKIP_COMMENTS.union([tokenize.STRING]):
            skip_lines.add(line)

    for token_type, text, start, end, line in tokens:
        # Skip lines that aren't pure strings
        if token_type == tokenize.STRING and skip_lines:
            continue
        if token_type in (tokenize.STRING, tokenize.COMMENT):
            # Only check comment-only lines
            if prev_token is None or prev_token in SKIP_TOKENS:
                lines = line.splitlines()
                for line_num, physical_line in enumerate(lines):
                    if start[0] + line_num == 1 and line.startswith('#!'):
                        return
                    length = len(physical_line)
                    chunks = physical_line.split()
                    if token_type == tokenize.COMMENT:
                        if (len(chunks) == 2 and
                                length - len(chunks[-1]) < MAX_DOC_LENGTH):
                            continue
                    if len(chunks) == 1 and line_num + 1 < len(lines):
                        if (len(chunks) == 1 and
                                length - len(chunks[-1]) < MAX_DOC_LENGTH):
                            continue
                    if length > max_doc_length:
                        doc_error = (start[0] + line_num, max_doc_length)
                        yield (doc_error, "W505 doc line too long "
                                          "(%d > %d characters)"
                               % (length, max_doc_length))
        prev_token = token_type

