
def hnm_harary_graph(n, m, create_using=None):
    r"""Return the Harary graph with given numbers of nodes and edges.

    The Harary graph $H_{n, m}$ is the graph that maximizes node connectivity
    with $n$ nodes and $m$ edges.

    This maximum node connectivity is known to be $\lfloor 2m/n \rfloor$. [1]_

    Parameters
    ----------
    n: integer
        The number of nodes the generated graph is to contain.

    m: integer
        The number of edges the generated graph is to contain.

    create_using : NetworkX graph constructor, optional (default=nx.Graph)
        Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    NetworkX graph
        The Harary graph $H_{n, m}$.

    See Also
    --------
    hkn_harary_graph

    Notes
    -----
    This algorithm runs in $O(m)$ time.
    The implementation follows [2]_.

    References
    ----------
    .. [1] F. T. Boesch, A. Satyanarayana, and C. L. Suffel,
       "A Survey of Some Network Reliability Analysis and Synthesis Results,"
       Networks, pp. 99-107, 2009.

    .. [2] Harary, F. "The Maximum Connectivity of a Graph."
       Proc. Nat. Acad. Sci. USA 48, 1142-1146, 1962.
    """

    if n < 1:
        raise NetworkXError("The number of nodes must be >= 1!")
    if m < n - 1:
        raise NetworkXError("The number of edges must be >= n - 1 !")
    if m > n * (n - 1) // 2:
        raise NetworkXError("The number of edges must be <= n(n-1)/2")

    # Get the floor of average node degree.
    d = 2 * m // n

    offset = d // 2
    H = nx.circulant_graph(n, range(1, offset + 1), create_using=create_using)

    half = n // 2
    if (n % 2 == 0) or (d % 2 == 0):
        # If d is odd; n must be even.
        if d % 2 == 1:
            # Add edges diagonally.
            H.add_edges_from((i, i + half) for i in range(half))

        r = 2 * m % n
        # Add remaining edges at offset + 1.
        H.add_edges_from((i, i + offset + 1) for i in range(r // 2))
    else:
        # Add the remaining m - n * offset edges between i and i + half.
        H.add_edges_from((i, (i + half) % n) for i in range(m - n * offset))

    return H

