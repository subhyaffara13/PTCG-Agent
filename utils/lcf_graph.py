
def LCF_graph(n, shift_list, repeats, create_using=None):
    """
    Return the cubic graph specified in LCF notation.

    LCF (Lederberg-Coxeter-Fruchte) notation[1]_ is a compressed
    notation used in the generation of various cubic Hamiltonian
    graphs of high symmetry. See, for example, `dodecahedral_graph`,
    `desargues_graph`, `heawood_graph` and `pappus_graph`.

    Nodes are drawn from ``range(n)``. Each node ``n_i`` is connected with
    node ``n_i + shift % n`` where ``shift`` is given by cycling through
    the input `shift_list` `repeat` s times.

    Parameters
    ----------
    n : int
       The starting graph is the `n`-cycle with nodes ``0, ..., n-1``.
       The null graph is returned if `n` < 1.

    shift_list : list
       A list of integer shifts mod `n`, ``[s1, s2, .., sk]``

    repeats : int
       Integer specifying the number of times that shifts in `shift_list`
       are successively applied to each current node in the n-cycle
       to generate an edge between ``n_current`` and ``n_current + shift mod n``.

    Returns
    -------
    G : Graph
       A graph instance created from the specified LCF notation.

    Examples
    --------
    The utility graph $K_{3,3}$

    >>> G = nx.LCF_graph(6, [3, -3], 3)
    >>> G.edges()
    EdgeView([(0, 1), (0, 5), (0, 3), (1, 2), (1, 4), (2, 3), (2, 5), (3, 4), (4, 5)])

    The Heawood graph:

    >>> G = nx.LCF_graph(14, [5, -5], 7)
    >>> nx.is_isomorphic(G, nx.heawood_graph())
    True

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/LCF_notation

    """
    if n <= 0:
        return empty_graph(0, create_using)

    # start with the n-cycle
    G = cycle_graph(n, create_using)
    if G.is_directed():
        raise NetworkXError("Directed Graph not supported")
    G.name = "LCF_graph"
    nodes = sorted(G)

    n_extra_edges = repeats * len(shift_list)
    # edges are added n_extra_edges times
    # (not all of these need be new)
    if n_extra_edges < 1:
        return G

    for i in range(n_extra_edges):
        shift = shift_list[i % len(shift_list)]  # cycle through shift_list
        v1 = nodes[i % n]  # cycle repeatedly through nodes
        v2 = nodes[(i + shift) % n]
        G.add_edge(v1, v2)
    return G

