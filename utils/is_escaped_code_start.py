
def is_escaped_code_start(line, ext):
    """Is the current line a possibly commented code start marker?"""
    return _ESCAPED_CODE_START[ext].match(line)

