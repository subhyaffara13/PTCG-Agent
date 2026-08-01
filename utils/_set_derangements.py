
def _set_derangements(s):
    """
    yield derangements of items in ``s`` which are assumed to contain
    no repeated elements
    """
    if len(s) < 2:
        return
    if len(s) == 2:
        yield [s[1], s[0]]
        return
    if len(s) == 3:
        yield [s[1], s[2], s[0]]
        yield [s[2], s[0], s[1]]
        return
    for p in permutations(s):
        if not any(i == j for i, j in zip(p, s)):
            yield list(p)

