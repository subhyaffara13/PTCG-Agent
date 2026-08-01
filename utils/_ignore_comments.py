
def _ignore_comments(lines_enum):
    """
    Strips comments and filter empty lines.
    """
    for line_number, line in lines_enum:
        line = COMMENT_RE.sub("", line)
        line = line.strip()
        if line:
            yield line_number, line

