
def random_labeled_tree(n, *, seed=None):
    """Returns a labeled tree on `n` nodes chosen uniformly at random.

    Generating uniformly distributed random Prüfer sequences and
    converting them into the corresponding trees is a straightforward
    method of generating uniformly distributed random labeled trees.
    This function implements this method.

    Parameters
    ----------
    n : int
        The number of nodes, greater than zero.
    seed : random_state
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`

    Returns
    -------
     :class:`networkx.Graph`
        A `networkx.Graph` with nodes in the set {0, …, *n* - 1}.

    Raises
    ------
    NetworkXPointlessConcept
        If `n` is zero (because the null graph is not a tree).

    Examples
    --------
    >>> G = nx.random_labeled_tree(5, seed=42)
    >>> nx.is_tree(G)
    True
    >>> G.edges
    EdgeView([(0, 1), (0, 3), (0, 2), (2, 4)])

    A tree with *arbitrarily directed* edges can be created by assigning
    generated edges to a ``DiGraph``:

    >>> DG = nx.DiGraph()
    >>> DG.add_edges_from(G.edges)
    >>> nx.is_tree(DG)
    True
    >>> DG.edges
    OutEdgeView([(0, 1), (0, 3), (0, 2), (2, 4)])
    """
    # Cannot create a Prüfer sequence unless `n` is at least two.
    if n == 0:
        raise nx.NetworkXPointlessConcept("the null graph is not a tree")
    if n == 1:
        return nx.empty_graph(1)
    return nx.from_prufer_sequence([seed.choice(range(n)) for i in range(n - 2)])

