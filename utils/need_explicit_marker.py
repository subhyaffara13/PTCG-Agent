
def need_explicit_marker(source, language="python", global_escape_flag=True, explicitly_code=True):
    """Does this code needs an explicit cell marker?"""
    if language != "python" or not global_escape_flag or not explicitly_code:
        return False

    parser = StringParser(language)
    for line in source:
        if not parser.is_quoted() and is_magic(line, language, global_escape_flag, explicitly_code):
            if not is_magic(line, language, global_escape_flag, False):
                return True
        parser.read_line(line)
    return False

