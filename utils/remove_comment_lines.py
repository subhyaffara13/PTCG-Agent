
def remove_comment_lines(a: list[str]) -> list[str]:
    """Return a copy of array with comments removed.

    Lines starting with '--' (but not with '---') are removed.
    """
    r = []
    for s in a:
        if s.strip().startswith("--") and not s.strip().startswith("---"):
            pass
        else:
            r.append(s)
    return r

