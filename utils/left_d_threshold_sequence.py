
def left_d_threshold_sequence(n, m):
    """
    Returns a "left-dominated" threshold sequence with `n` vertices and `m` edges.

    Each vertex in the sequence is either dominant or isolated.
    In the "left-dominated" version, once the basic sequence is formed,
    isolated vertices may be flipped to dominant from the left in order
    to reach the target number of edges.

    Parameters
    ----------
    n : int
        Number of vertices.
    m : int
        Number of edges.

    Returns
    -------
    A list of 'd' (dominant) and 'i' (isolated) forming a left-dominated threshold sequence.

    Raises
    ------
    ValueError
        If `m` exceeds the maximum number of edges.

    Examples
    --------
    For certain small cases, both left and right dominated versions produce
    the same sequence. However, for larger values of `m`, the difference in
    flipping order becomes evident. For instance, compare the sequences for
    ``n=6, m=8``:

    >>> from networkx.algorithms.threshold import left_d_threshold_sequence
    >>> seq = left_d_threshold_sequence(6, 8)
    >>> seq
    ['d', 'd', 'd', 'i', 'i', 'd']

    In contrast, the right-dominated version yields:

    >>> from networkx.algorithms.threshold import right_d_threshold_sequence
    >>> right_seq = right_d_threshold_sequence(6, 8)
    >>> right_seq
    ['d', 'i', 'i', 'd', 'i', 'd']
    """

    cs = ["d"] + ["i"] * (n - 1)  # create sequence with n insolated nodes

    #  m <n : not enough edges, make disconnected
    if m < n:
        cs[m] = "d"
        return cs

    # too many edges
    if m > n * (n - 1) / 2:
        raise ValueError("Too many edges for this many nodes.")

    # Connected case when M>N-1
    cs[n - 1] = "d"
    sum = n - 1
    ind = 1
    while sum < m:
        cs[ind] = "d"
        sum += ind
        ind += 1
    if sum > m:  # be sure not to change the first vertex
        cs[sum - m] = "i"
    return cs

