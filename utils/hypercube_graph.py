
def hypercube_graph(n):
    """Returns the *n*-dimensional hypercube graph.

    The *n*-dimensional hypercube graph [1]_ has ``2**n`` nodes, each represented as
    a binary integer in the form of a tuple of 0's and 1's. Edges exist between
    nodes that differ in exactly one bit.

    Parameters
    ----------
    n : int
        Dimension of the hypercube, must be a positive integer.

    Returns
    -------
    networkx.Graph
        The n-dimensional hypercube graph as an undirected graph.

    See Also
    --------
    grid_2d_graph, triangular_lattice_graph, hexagonal_lattice_graph :
        2D lattice graphs
    grid_graph :
        A more general N-dimensional grid

    Examples
    --------
    >>> G = nx.hypercube_graph(3)
    >>> list(G.neighbors((0, 0, 0)))
    [(1, 0, 0), (0, 1, 0), (0, 0, 1)]

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Hypercube_graph
    """
    dim = n * [2]
    G = grid_graph(dim)
    return G

