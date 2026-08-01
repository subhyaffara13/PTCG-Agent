
def min_edge_dominating_set(G):
    r"""Returns minimum cardinality edge dominating set.

    Parameters
    ----------
    G : NetworkX graph
      Undirected graph

    Returns
    -------
    min_edge_dominating_set : set
      Returns a set of dominating edges whose size is no more than 2 * OPT.

    Examples
    --------
    >>> G = nx.petersen_graph()
    >>> nx.approximation.min_edge_dominating_set(G)
    {(0, 1), (4, 9), (6, 8), (5, 7), (2, 3)}

    Raises
    ------
    ValueError
        If the input graph `G` is empty.

    Notes
    -----
    The algorithm computes an approximate solution to the edge dominating set
    problem. The result is no more than 2 * OPT in terms of size of the set.
    Runtime of the algorithm is $O(|E|)$.
    """
    if not G:
        raise ValueError("Expected non-empty NetworkX graph!")
    return maximal_matching(G)

