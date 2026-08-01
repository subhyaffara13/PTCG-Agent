
def dual_barabasi_albert_graph(
    n, m1, m2, p, seed=None, initial_graph=None, *, create_using=None
):
    """Returns a random graph using dual Barabási–Albert preferential attachment

    A graph of $n$ nodes is grown by attaching new nodes each with either $m_1$
    edges (with probability $p$) or $m_2$ edges (with probability $1-p$) that
    are preferentially attached to existing nodes with high degree.

    Parameters
    ----------
    n : int
        Number of nodes
    m1 : int
        Number of edges to link each new node to existing nodes with probability $p$
    m2 : int
        Number of edges to link each new node to existing nodes with probability $1-p$
    p : float
        The probability of attaching $m_1$ edges (as opposed to $m_2$ edges)
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    initial_graph : Graph or None (default)
        Initial network for Barabási–Albert algorithm.
        A copy of `initial_graph` is used.
        It should be connected for most use cases.
        If None, starts from an star graph on max(m1, m2) + 1 nodes.
    create_using : Graph constructor, optional (default=nx.Graph)
        Graph type to create. If graph instance, then cleared before populated.
        Multigraph and directed types are not supported and raise a ``NetworkXError``.

    Returns
    -------
    G : Graph

    Raises
    ------
    NetworkXError
        If `m1` and `m2` do not satisfy ``1 <= m1,m2 < n``, or
        `p` does not satisfy ``0 <= p <= 1``, or
        the initial graph number of nodes m0 does not satisfy m1, m2 <= m0 <= n.

    References
    ----------
    .. [1] N. Moshiri "The dual-Barabasi-Albert model", arXiv:1810.10538.
    """
    create_using = check_create_using(create_using, directed=False, multigraph=False)
    if m1 < 1 or m1 >= n:
        raise nx.NetworkXError(
            f"Dual Barabási–Albert must have m1 >= 1 and m1 < n, m1 = {m1}, n = {n}"
        )
    if m2 < 1 or m2 >= n:
        raise nx.NetworkXError(
            f"Dual Barabási–Albert must have m2 >= 1 and m2 < n, m2 = {m2}, n = {n}"
        )
    if p < 0 or p > 1:
        raise nx.NetworkXError(
            f"Dual Barabási–Albert network must have 0 <= p <= 1, p = {p}"
        )

    # For simplicity, if p == 0 or 1, just return BA
    if p == 1:
        return barabasi_albert_graph(n, m1, seed, create_using=create_using)
    elif p == 0:
        return barabasi_albert_graph(n, m2, seed, create_using=create_using)

    if initial_graph is None:
        # Default initial graph : star graph on max(m1, m2) nodes
        G = star_graph(max(m1, m2), create_using)
    else:
        if len(initial_graph) < max(m1, m2) or len(initial_graph) > n:
            raise nx.NetworkXError(
                f"Barabási–Albert initial graph must have between "
                f"max(m1, m2) = {max(m1, m2)} and n = {n} nodes"
            )
        G = initial_graph.copy()

    # Target nodes for new edges
    targets = list(G)
    # List of existing nodes, with nodes repeated once for each adjacent edge
    repeated_nodes = [n for n, d in G.degree() for _ in range(d)]
    # Start adding the remaining nodes.
    source = len(G)
    while source < n:
        # Pick which m to use (m1 or m2)
        if seed.random() < p:
            m = m1
        else:
            m = m2
        # Now choose m unique nodes from the existing nodes
        # Pick uniformly from repeated_nodes (preferential attachment)
        targets = _random_subset(repeated_nodes, m, seed)
        # Add edges to m nodes from the source.
        G.add_edges_from(zip([source] * m, targets))
        # Add one node to the list for each new edge just created.
        repeated_nodes.extend(targets)
        # And the new node "source" has m edges to add to the list.
        repeated_nodes.extend([source] * m)

        source += 1
    return G

