
def unesc(line, language):
    """Uncomment once a commented line"""
    comment = _COMMENT[language]
    unindented = line.lstrip()
    indent = line[: len(line) - len(unindented)]
    if unindented.startswith(comment + " "):
        return indent + unindented[len(comment) + 1 :]
    if unindented.startswith(comment):
        return indent + unindented[len(comment) :]
    return line

