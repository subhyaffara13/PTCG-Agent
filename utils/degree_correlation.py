
def degree_correlation(creation_sequence):
    """
    Return the degree-degree correlation over all edges.
    """
    cs = creation_sequence
    s1 = 0  # deg_i*deg_j
    s2 = 0  # deg_i^2+deg_j^2
    s3 = 0  # deg_i+deg_j
    m = 0  # number of edges
    rd = cs.count("d")  # number of d nodes to the right
    rdi = [i for i, sym in enumerate(cs) if sym == "d"]  # index of "d"s
    ds = degree_sequence(cs)
    for i, sym in enumerate(cs):
        if sym == "d":
            rdi.pop(0)
        degi = ds[i]
        for dj in rdi:
            degj = ds[dj]
            s1 += degj * degi
            s2 += degi**2 + degj**2
            s3 += degi + degj
            m += 1
    denom = 2 * m * s2 - s3 * s3
    numer = 4 * m * s1 - s3 * s3
    if denom == 0:
        if numer == 0:
            return 1
        raise ValueError(f"Zero Denominator but Numerator is {numer}")
    return numer / denom

