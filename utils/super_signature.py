
def super_signature(signatures):
    """A signature that would break ambiguities"""
    n = len(signatures[0])
    if not all(len(s) == n for s in signatures):
        raise AssertionError("All signatures must have the same length")

    return [max((type.mro(sig[i]) for sig in signatures), key=len)[0] for i in range(n)]


def super_signature(signatures):
    """ A signature that would break ambiguities """
    n = len(signatures[0])
    assert all(len(s) == n for s in signatures)

    return [max([type.mro(sig[i]) for sig in signatures], key=len)[0]
               for i in range(n)]

