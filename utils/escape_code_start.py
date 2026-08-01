
def escape_code_start(source, ext, language="python"):
    """Escape code start with '# '"""
    parser = StringParser(language)
    for pos, line in enumerate(source):
        if not parser.is_quoted() and is_escaped_code_start(line, ext):
            source[pos] = _SCRIPT_EXTENSIONS.get(ext, {}).get("comment", "#") + " " + line
        parser.read_line(line)
    return source

