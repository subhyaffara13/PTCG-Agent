
def iscommentline(line: str) -> bool:
    c = line.lstrip()[:1]
    return c in COMMENTCHARS

