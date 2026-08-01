
def read_fenced_cell(token, cell_index, cell_type):
    """Parse (and validate) the full directive text."""
    content = token.content
    error_msg = f"{cell_type} cell {cell_index} at line {token.map[0] + 1} could not be read: "

    body_lines, options = parse_directive_options(content, error_msg)

    # remove first line of body if blank
    # this is to allow space between the options and the content
    if body_lines and not body_lines[0].strip():
        body_lines = body_lines[1:]

    return options, body_lines

