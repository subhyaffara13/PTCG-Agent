
def subgraph_centrality(G, *, normalized=False):
    r"""Returns subgraph centrality for each node in G.

    Subgraph centrality  of a node `n` is the sum of weighted closed
    walks of all lengths starting and ending at node `n`. The weights
    decrease with path length. Each closed walk is associated with a
    connected subgraph ([1]_).

    Parameters
    ----------
    G: Graph
    normalized : bool
        If True, normalize the centrality values using the largest eigenvalue of the
        adjacency matrix so that the centrality values are generally between 0 and 1.

    Returns
    -------
    nodes : dictionary
       Dictionary of nodes with subgraph centrality as the value.

    Raises
    ------
    NetworkXError
       If the graph is not undirected and simple.

    See Also
    --------
    subgraph_centrality_exp:
        Alternative algorithm of the subgraph centrality for each node of G.

    Notes
    -----
    This version of the algorithm computes eigenvalues and eigenvectors
    of the adjacency matrix.

    Subgraph centrality of a node `u` in G can be found using
    a spectral decomposition of the adjacency matrix [1]_,

    .. math::

       SC(u)=\sum_{j=1}^{N}(v_{j}^{u})^2 e^{\lambda_{j}},

    where `v_j` is an eigenvector of the adjacency matrix `A` of G
    corresponding to the eigenvalue `\lambda_j`.

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
    >>> sc = nx.subgraph_centrality(G)
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
    import numpy as np

    nodelist = list(G)  # ordering of nodes in matrix
    A = nx.to_numpy_array(G, nodelist)
    # convert to 0-1 matrix
    A[np.nonzero(A)] = 1
    w, v = np.linalg.eigh(A)
    vsquare = np.array(v) ** 2
    if normalized:
        expw = np.exp(w - w.max())
    else:
        expw = np.exp(w)
    xg = vsquare @ expw
    # convert vector dictionary keyed by node
    sc = dict(zip(nodelist, map(float, xg)))
    return sc

