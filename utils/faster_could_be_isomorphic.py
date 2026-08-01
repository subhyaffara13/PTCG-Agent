
def faster_could_be_isomorphic(G1, G2):
    """Returns False if graphs are definitely not isomorphic.

    True does NOT guarantee isomorphism.

    Parameters
    ----------
    G1, G2 : graphs
       The two graphs G1 and G2 must be the same type.

    Notes
    -----
    Checks for matching degree sequences.
    """
    # Check global properties
    if G1.order() != G2.order():
        return False

    # Check local properties
    d1 = sorted(d for n, d in G1.degree())
    d2 = sorted(d for n, d in G2.degree())

    if d1 != d2:
        return False

    # OK...
    return True

