
def diameter(G, e=None, usebounds=False, weight=None):
    """Returns the diameter of the graph G.

    The diameter is the maximum eccentricity.

    Parameters
    ----------
    G : NetworkX graph
       A graph

    e : eccentricity dictionary, optional
      A precomputed dictionary of eccentricities.

    usebounds : bool, optional
        If `True`, use extrema bounding (see Notes) when computing the diameter
        for undirected graphs. Extrema bounding may accelerate the
        distance calculation for some graphs. `usebounds` is ignored if `G` is
        directed or if `e` is not `None`. Default is `False`.

    weight : string, function, or None
        If this is a string, then edge weights will be accessed via the
        edge attribute with this key (that is, the weight of the edge
        joining `u` to `v` will be ``G.edges[u, v][weight]``). If no
        such edge attribute exists, the weight of the edge is assumed to
        be one.

        If this is a function, the weight of an edge is the value
        returned by the function. The function must accept exactly three
        positional arguments: the two endpoints of an edge and the
        dictionary of edge attributes for that edge. The function must
        return a number.

        If this is None, every edge has weight/distance/cost 1.

        Weights stored as floating point values can lead to small round-off
        errors in distances. Use integer weights to avoid this.

        Weights should be positive, since they are distances.

    Returns
    -------
    d : integer
       Diameter of graph

    Notes
    -----
    When ``usebounds=True``, the computation makes use of smart lower
    and upper bounds and is often linear in the number of nodes, rather than
    quadratic (except for some border cases such as complete graphs or circle
    shaped-graphs).

    Examples
    --------
    >>> G = nx.Graph([(1, 2), (1, 3), (1, 4), (3, 4), (3, 5), (4, 5)])
    >>> nx.diameter(G)
    3

    See Also
    --------
    eccentricity
    """
    if usebounds is True and e is None and not G.is_directed():
        return _extrema_bounding(G, compute="diameter", weight=weight)
    if e is None:
        e = eccentricity(G, weight=weight)
    return max(e.values())


def diameter(G, seed=None):
    """Returns a lower bound on the diameter of the graph G.

    The function computes a lower bound on the diameter (i.e., the maximum eccentricity)
    of a directed or undirected graph G. The procedure used varies depending on the graph
    being directed or not.

    If G is an `undirected` graph, then the function uses the `2-sweep` algorithm [1]_.
    The main idea is to pick the farthest node from a random node and return its eccentricity.

    Otherwise, if G is a `directed` graph, the function uses the `2-dSweep` algorithm [2]_,
    The procedure starts by selecting a random source node $s$ from which it performs a
    forward and a backward BFS. Let $a_1$ and $a_2$ be the farthest nodes in the forward and
    backward cases, respectively. Then, it computes the backward eccentricity of $a_1$ using
    a backward BFS and the forward eccentricity of $a_2$ using a forward BFS.
    Finally, it returns the best lower bound between the two.

    In both cases, the time complexity is linear with respect to the size of G.

    Parameters
    ----------
    G : NetworkX graph

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    d : integer
       Lower Bound on the Diameter of G

    Examples
    --------
    >>> G = nx.path_graph(10)  # undirected graph
    >>> nx.diameter(G)
    9
    >>> G = nx.cycle_graph(3, create_using=nx.DiGraph)  # directed graph
    >>> nx.diameter(G)
    2

    Raises
    ------
    NetworkXError
        If the graph is empty or
        If the graph is undirected and not connected or
        If the graph is directed and not strongly connected.

    See Also
    --------
    networkx.algorithms.distance_measures.diameter

    References
    ----------
    .. [1] Magnien, Clémence, Matthieu Latapy, and Michel Habib.
       *Fast computation of empirically tight bounds for the diameter of massive graphs.*
       Journal of Experimental Algorithmics (JEA), 2009.
       https://arxiv.org/pdf/0904.2728.pdf
    .. [2] Crescenzi, Pierluigi, Roberto Grossi, Leonardo Lanzi, and Andrea Marino.
       *On computing the diameter of real-world directed (weighted) graphs.*
       International Symposium on Experimental Algorithms. Springer, Berlin, Heidelberg, 2012.
       https://courses.cs.ut.ee/MTAT.03.238/2014_fall/uploads/Main/diameter.pdf
    """
    # if G is empty
    if not G:
        raise nx.NetworkXError("Expected non-empty NetworkX graph!")
    # if there's only a node
    if G.number_of_nodes() == 1:
        return 0
    # if G is directed
    if G.is_directed():
        return _two_sweep_directed(G, seed)
    # else if G is undirected
    return _two_sweep_undirected(G, seed)

