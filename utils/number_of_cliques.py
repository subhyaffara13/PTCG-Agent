
def number_of_cliques(G, nodes=None, cliques=None):
    """Return the number of maximal cliques each node is part of.

    Output is a single value or dict depending on `nodes`.
    Optional list of cliques can be input if already computed.

    Parameters
    ----------
    G : NetworkX graph
        An undirected graph.

    nodes : list or None, optional (default=None)
        A list of nodes to return the number of maximal cliques for.
        If `None`, return the number of maximal cliques for all nodes.

    cliques : list or None, optional (default=None)
        A precomputed list of maximal cliques to use for the calculation.

    Returns
    -------
    int or dict
        If `nodes` is a single node, return the number of maximal cliques it is
        part of. If `nodes` is a list, return a dictionary keyed by node to the
        number of maximal cliques it is part of.

    Raises
    ------
    NetworkXNotImplemented
        If `G` is directed.

    See Also
    --------
    find_cliques
    node_clique_number

    Examples
    --------
    Compute the number of maximal cliques a node is part of:

    >>> G = nx.complete_graph(3)
    >>> nx.add_cycle(G, [0, 3, 4])
    >>> nx.number_of_cliques(G, nodes=0)
    2
    >>> nx.number_of_cliques(G, nodes=1)
    1

    Or, for a list of nodes:

    >>> nx.number_of_cliques(G, nodes=[0, 1])
    {0: 2, 1: 1}

    If no explicit `nodes` are provided, all nodes are considered:

    >>> nx.number_of_cliques(G)
    {0: 2, 1: 1, 2: 1, 3: 1, 4: 1}

    The list of maximal cliques can also be precomputed:

    >>> cl = list(nx.find_cliques(G))
    >>> nx.number_of_cliques(G, cliques=cl)
    {0: 2, 1: 1, 2: 1, 3: 1, 4: 1}
    """
    if cliques is None:
        cliques = find_cliques(G)

    if nodes is None:
        nodes = list(G.nodes())  # none, get entire graph

    if not isinstance(nodes, list):  # check for a list
        v = nodes
        # assume it is a single value
        numcliq = sum(1 for c in cliques if v in c)
    else:
        numcliq = Counter(chain.from_iterable(cliques))
        numcliq = {v: numcliq[v] for v in nodes}  # return a dict
    return numcliq

