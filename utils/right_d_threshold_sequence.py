
def right_d_threshold_sequence(n, m):
    """
    Returns a "right-dominated" threshold sequence with `n` vertices and `m` edges.

    Each vertex in the sequence is either dominant or isolated.
    In the "right-dominated" version, once the basic sequence is formed,
    isolated vertices may be flipped to dominant from the right in order
    to reach the target number of edges.

    Parameters
    ----------
    n : int
        Number of vertices.
    m : int
        Number of edges.

    Returns
    -------
    A list of 'd' (dominant) and 'i' (isolated) forming a right-dominated threshold sequence.

    Raises
    ------
    ValueError
        If `m` exceeds the maximum number of edges.

    Examples
    --------
    >>> from networkx.algorithms.threshold import right_d_threshold_sequence
    >>> right_d_threshold_sequence(5, 3)
    ['d', 'i', 'i', 'd', 'i']
    """

    cs = ["d"] + ["i"] * (n - 1)  # create sequence with n insolated nodes

    #  m <n : not enough edges, make disconnected
    if m < n:
        cs[m] = "d"
        return cs

    # too many edges
    if m > n * (n - 1) / 2:
        raise ValueError("Too many edges for this many nodes.")

    # connected case m >n-1
    ind = n - 1
    sum = n - 1
    while sum < m:
        cs[ind] = "d"
        ind -= 1
        sum += ind
    ind = m - (sum - ind)
    cs[ind] = "d"
    return cs

