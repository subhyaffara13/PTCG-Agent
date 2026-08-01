
def hkn_harary_graph(k, n, create_using=None):
    r"""Return the Harary graph with given node connectivity and node number.

    The Harary graph $H_{k, n}$ is the graph that minimizes the number of
    edges needed with given node connectivity $k$ and node number $n$.

    This smallest number of edges is known to be $\lceil kn/2 \rceil$ [1]_.

    Parameters
    ----------
    k: integer
        The node connectivity of the generated graph.

    n: integer
        The number of nodes the generated graph is to contain.

    create_using : NetworkX graph constructor, optional (default=nx.Graph)
        Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    NetworkX graph
        The Harary graph $H_{k, n}$.

    See Also
    --------
    hnm_harary_graph

    Notes
    -----
    This algorithm runs in $O(kn)$ time.
    The implementation follows [2]_.

    References
    ----------
    .. [1] Weisstein, Eric W. "Harary Graph." From MathWorld--A Wolfram Web
     Resource. http://mathworld.wolfram.com/HararyGraph.html.

    .. [2] Harary, F. "The Maximum Connectivity of a Graph."
      Proc. Nat. Acad. Sci. USA 48, 1142-1146, 1962.
    """

    if k < 1:
        raise NetworkXError("The node connectivity must be >= 1!")
    if n < k + 1:
        raise NetworkXError("The number of nodes must be >= k+1 !")

    # In case of connectivity 1, simply return the path graph.
    if k == 1:
        return nx.path_graph(n, create_using)

    offset = k // 2
    H = nx.circulant_graph(n, range(1, offset + 1), create_using=create_using)

    half = n // 2
    if (k % 2 == 0) or (n % 2 == 0):
        # If k is odd; n must be even.
        if k % 2 == 1:
            # Add edges diagonally.
            H.add_edges_from((i, i + half) for i in range(half))
    else:
        # Add half + 1 edges between i and i + half.
        H.add_edges_from((i, (i + half) % n) for i in range(half + 1))

    return H

