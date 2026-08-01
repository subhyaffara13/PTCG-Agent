
def strip_list(l: list[str]) -> list[str]:
    """Return a stripped copy of l.

    Strip whitespace at the end of all lines, and strip all empty
    lines from the end of the array.
    """

    r: list[str] = []
    for s in l:
        # Strip spaces at end of line
        r.append(re.sub(r"\s+$", "", s))

    while r and r[-1] == "":
        r.pop()

    return r

