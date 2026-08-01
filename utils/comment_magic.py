
def comment_magic(source, language="python", global_escape_flag=True, explicitly_code=True):
    """Escape Jupyter magics with '# '"""
    parser = StringParser(language)
    next_is_magic = False
    for pos, line in enumerate(source):
        if not parser.is_quoted() and (next_is_magic or is_magic(line, language, global_escape_flag, explicitly_code)):
            if next_is_magic:
                # this is the continuation line of a magic command on the previous line,
                # so we don't want to indent the comment
                unindented = line
                indent = ""
            else:
                unindented = line.lstrip()
                indent = line[: len(line) - len(unindented)]
            source[pos] = indent + _COMMENT[language] + " " + unindented
            next_is_magic = language == "python" and _LINE_CONTINUATION_RE.match(line)
        parser.read_line(line)
    return source

