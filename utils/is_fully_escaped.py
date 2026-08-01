
def is_fully_escaped(s: str) -> bool:
    # we know we won't compile with re.VERBOSE, so whitespace doesn't need to be escaped
    metacharacters = "{}()+.*?^$[]|"
    # Strip all escape sequences (backslash + any char), then check if any
    # metacharacter remains unescaped in the resulting string.
    stripped = re.sub(r"\\.", "", s)
    return not any(c in metacharacters for c in stripped)

