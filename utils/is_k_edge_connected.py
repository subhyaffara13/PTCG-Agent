
def is_k_edge_connected(G, k):
    """Tests to see if a graph is k-edge-connected.

    Is it impossible to disconnect the graph by removing fewer than k edges?
    If so, then G is k-edge-connected.

    Parameters
    ----------
    G : NetworkX graph
       An undirected graph.

    k : integer
        edge connectivity to test for

    Returns
    -------
    boolean
        True if G is k-edge-connected.

    See Also
    --------
    :func:`is_locally_k_edge_connected`

    Examples
    --------
    >>> G = nx.barbell_graph(10, 0)
    >>> nx.is_k_edge_connected(G, k=1)
    True
    >>> nx.is_k_edge_connected(G, k=2)
    False
    """
    if k < 1:
        raise ValueError(f"k must be positive, not {k}")
    # First try to quickly determine if G is not k-edge-connected
    if G.number_of_nodes() < k + 1:
        return False
    elif any(d < k for n, d in G.degree()):
        return False
    else:
        # Otherwise perform the full check
        if k == 1:
            return nx.is_connected(G)
        elif k == 2:
            return nx.is_connected(G) and not nx.has_bridges(G)
        else:
            return nx.edge_connectivity(G, cutoff=k) >= k

