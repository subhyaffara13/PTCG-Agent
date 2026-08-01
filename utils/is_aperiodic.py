
def is_aperiodic(G):
    """Returns True if `G` is aperiodic.

    A strongly connected directed graph is aperiodic if there is no integer ``k > 1``
    that divides the length of every cycle in the graph.

    This function requires the graph `G` to be strongly connected and will raise
    an error if it's not. For graphs that are not strongly connected, you should
    first identify their strongly connected components
    (using :func:`~networkx.algorithms.components.strongly_connected_components`)
    or attracting components
    (using :func:`~networkx.algorithms.components.attracting_components`),
    and then apply this function to those individual components.

    Parameters
    ----------
    G : NetworkX DiGraph
        A directed graph

    Returns
    -------
    bool
        True if the graph is aperiodic False otherwise

    Raises
    ------
    NetworkXError
        If `G` is not directed
    NetworkXError
        If `G` is not strongly connected
    NetworkXPointlessConcept
        If `G` has no nodes

    Examples
    --------
    A graph consisting of one cycle, the length of which is 2. Therefore ``k = 2``
    divides the length of every cycle in the graph and thus the graph
    is *not aperiodic*::

        >>> DG = nx.DiGraph([(1, 2), (2, 1)])
        >>> nx.is_aperiodic(DG)
        False

    A graph consisting of two cycles: one of length 2 and the other of length 3.
    The cycle lengths are coprime, so there is no single value of k where ``k > 1``
    that divides each cycle length and therefore the graph is *aperiodic*::

        >>> DG = nx.DiGraph([(1, 2), (2, 3), (3, 1), (1, 4), (4, 1)])
        >>> nx.is_aperiodic(DG)
        True

    A graph created from cycles of the same length can still be aperiodic since
    the cycles can overlap and form new cycles of different lengths. For example,
    the following graph contains a cycle ``[4, 2, 3, 1]`` of length 4, which is coprime
    with the explicitly added cycles of length 3, so the graph is aperiodic::

        >>> DG = nx.DiGraph()
        >>> nx.add_cycle(DG, [1, 2, 3])
        >>> nx.add_cycle(DG, [2, 1, 4])
        >>> nx.is_aperiodic(DG)
        True

    A single-node graph's aperiodicity depends on whether it has a self-loop:
    it is aperiodic if a self-loop exists, and periodic otherwise::

        >>> G = nx.DiGraph()
        >>> G.add_node(1)
        >>> nx.is_aperiodic(G)
        False
        >>> G.add_edge(1, 1)
        >>> nx.is_aperiodic(G)
        True

    A Markov chain can be modeled as a directed graph, with nodes representing
    states and edges representing transitions with non-zero probability.
    Aperiodicity is typically considered for irreducible Markov chains,
    which are those that are *strongly connected* as graphs.

    The following Markov chain is irreducible and aperiodic, and thus
    ergodic. It is guaranteed to have a unique stationary distribution::

        >>> G = nx.DiGraph()
        >>> nx.add_cycle(G, [1, 2, 3, 4])
        >>> G.add_edge(1, 3)
        >>> nx.is_aperiodic(G)
        True

    Reducible Markov chains can sometimes have a unique stationary distribution.
    This occurs if the chain has exactly one closed communicating class and
    that class itself is aperiodic (see [1]_). You can use
    :func:`~networkx.algorithms.components.attracting_components`
    to find these closed communicating classes::

        >>> G = nx.DiGraph([(1, 3), (2, 3)])
        >>> nx.add_cycle(G, [3, 4, 5, 6])
        >>> nx.add_cycle(G, [3, 5, 6])
        >>> communicating_classes = list(nx.strongly_connected_components(G))
        >>> len(communicating_classes)
        3
        >>> closed_communicating_classes = list(nx.attracting_components(G))
        >>> len(closed_communicating_classes)
        1
        >>> nx.is_aperiodic(G.subgraph(closed_communicating_classes[0]))
        True

    Notes
    -----
    This uses the method outlined in [1]_, which runs in $O(m)$ time
    given $m$ edges in `G`.

    References
    ----------
    .. [1] Jarvis, J. P.; Shier, D. R. (1996),
       "Graph-theoretic analysis of finite Markov chains,"
       in Shier, D. R.; Wallenius, K. T., Applied Mathematical Modeling:
       A Multidisciplinary Approach, CRC Press.
    """
    if not G.is_directed():
        raise nx.NetworkXError("is_aperiodic not defined for undirected graphs")
    if len(G) == 0:
        raise nx.NetworkXPointlessConcept("Graph has no nodes.")
    if not nx.is_strongly_connected(G):
        raise nx.NetworkXError("Graph is not strongly connected.")
    s = arbitrary_element(G)
    levels = {s: 0}
    this_level = [s]
    g = 0
    lev = 1
    while this_level:
        next_level = []
        for u in this_level:
            for v in G[u]:
                if v in levels:  # Non-Tree Edge
                    g = gcd(g, levels[u] - levels[v] + 1)
                else:  # Tree Edge
                    next_level.append(v)
                    levels[v] = lev
        this_level = next_level
        lev += 1
    return g == 1

