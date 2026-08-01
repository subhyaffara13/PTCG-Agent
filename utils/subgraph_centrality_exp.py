
def subgraph_centrality_exp(G, *, normalized=False):
    r"""Returns the subgraph centrality for each node of G.

    Subgraph centrality  of a node `n` is the sum of weighted closed
    walks of all lengths starting and ending at node `n`. The weights
    decrease with path length. Each closed walk is associated with a
    connected subgraph ([1]_).

    Parameters
    ----------
    G: graph
    normalized : bool
        If True, normalize the centrality values using the largest eigenvalue of the
        adjacency matrix so that the centrality values are generally between 0 and 1.

    Returns
    -------
    nodes:dictionary
        Dictionary of nodes with subgraph centrality as the value.

    Raises
    ------
    NetworkXError
        If the graph is not undirected and simple.

    See Also
    --------
    subgraph_centrality:
        Alternative algorithm of the subgraph centrality for each node of G.

    Notes
    -----
    This version of the algorithm exponentiates the adjacency matrix.

    The subgraph centrality of a node `u` in G can be found using
    the matrix exponential of the adjacency matrix of G [1]_,

    .. math::

        SC(u)=(e^A)_{uu} .

    Examples
    --------
    (Example from [1]_)

    >>> G = nx.Graph(
    ...     [
    ...         (1, 2),
    ...         (1, 5),
    ...         (1, 8),
    ...         (2, 3),
    ...         (2, 8),
    ...         (3, 4),
    ...         (3, 6),
    ...         (4, 5),
    ...         (4, 7),
    ...         (5, 6),
    ...         (6, 7),
    ...         (7, 8),
    ...     ]
    ... )
    >>> sc = nx.subgraph_centrality_exp(G)
    >>> print([f"{node} {sc[node]:0.2f}" for node in sorted(sc)])
    ['1 3.90', '2 3.90', '3 3.64', '4 3.71', '5 3.64', '6 3.71', '7 3.64', '8 3.90']
    >>> sc = nx.subgraph_centrality(G, normalized=True)
    >>> print([f"{node} {sc[node]:0.3f}" for node in sorted(sc)])
    ['1 0.194', '2 0.194', '3 0.181', '4 0.184', '5 0.181', '6 0.184', '7 0.181', '8 0.194']

    References
    ----------
    .. [1] Ernesto Estrada, Juan A. Rodriguez-Velazquez,
       "Subgraph centrality in complex networks",
       Physical Review E 71, 056103 (2005).
       https://arxiv.org/abs/cond-mat/0504730

    """
    # alternative implementation that calculates the matrix exponential
    import scipy as sp

    nodelist = list(G)  # ordering of nodes in matrix
    A = nx.to_numpy_array(G, nodelist)
    # convert to 0-1 matrix
    A[A != 0.0] = 1
    expA = sp.linalg.expm(A)
    values = map(float, expA.diagonal())
    if normalized:
        values = values / values.max()
    # convert diagonal to dictionary keyed by node
    sc = dict(zip(nodelist, values))
    return sc

