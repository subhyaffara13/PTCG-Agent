
def mixing_dict(xy, normalized=False):
    """Returns a dictionary representation of mixing matrix.

    Parameters
    ----------
    xy : list or container of two-tuples
       Pairs of (x,y) items.

    attribute : string
       Node attribute key

    normalized : bool (default=False)
       Return counts if False or probabilities if True.

    Returns
    -------
    d: dictionary
       Counts or Joint probability of occurrence of values in xy.
    """
    d = {}
    psum = 0.0
    for x, y in xy:
        if x not in d:
            d[x] = {}
        if y not in d:
            d[y] = {}
        v = d[x].get(y, 0)
        d[x][y] = v + 1
        psum += 1

    if normalized:
        for _, jdict in d.items():
            for j in jdict:
                jdict[j] /= psum
    return d

