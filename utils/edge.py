
def edge(a, b, tie_breaker=hash):
    """A should be checked before B
    Tie broken by tie_breaker, defaults to ``hash``
    """
    if supercedes(a, b):
        if supercedes(b, a):
            return tie_breaker(a) > tie_breaker(b)
        else:
            return True
    return False


def edge(a, b, tie_breaker=hash):
    """A should be checked before B
    Tie broken by tie_breaker, defaults to ``hash``
    """
    # A either supersedes B and B does not supersede A or if B does then call
    # tie_breaker
    return supercedes(a, b) and (
        not supercedes(b, a) or tie_breaker(a) > tie_breaker(b)
    )


def edge(a, b, tie_breaker=hash):
    """ A should be checked before B

    Tie broken by tie_breaker, defaults to ``hash``
    """
    if supercedes(a, b):
        if supercedes(b, a):
            return tie_breaker(a) > tie_breaker(b)
        else:
            return True
    return False

