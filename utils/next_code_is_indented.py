
def next_code_is_indented(lines):
    """Is the next unescaped line indented?"""
    for line in lines:
        if _BLANK_LINE.match(line):
            continue
        return _PY_INDENTED.match(line)
    return False

