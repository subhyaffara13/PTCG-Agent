
def approximate_current_flow_betweenness_centrality(
    G,
    normalized=True,
    weight=None,
    dtype=float,
    solver="full",
    epsilon=0.5,
    kmax=10000,
    seed=None,
    *,
    sample_weight=1,
):
    r"""Compute the approximate current-flow betweenness centrality for nodes.

    Approximates the current-flow betweenness centrality within absolute
    error of epsilon with high probability [1]_.


    Parameters
    ----------
    G : graph
      A NetworkX graph

    normalized : bool, optional (default=True)
      If True the betweenness values are normalized by 2/[(n-1)(n-2)] where
      n is the number of nodes in G.

    weight : string or None, optional (default=None)
      Key for edge data used as the edge weight.
      If None, then use 1 as each edge weight.
      The weight reflects the capacity or the strength of the
      edge.

    dtype : data type (float)
      Default data type for internal matrices.
      Set to np.float32 for lower memory consumption.

    solver : string (default='full')
       Type of linear solver to use for computing the flow matrix.
       Options are "full" (uses most memory), "lu" (recommended), and
       "cg" (uses least memory).

    epsilon: float
        Absolute error tolerance. Note that smaller values of `epsilon` lead to
        higher numbers of sample pairs (``k``) and thus more computation time. The number
        of sample pairs is approximately ``(c/epsilon)^2 * log(n)`` where ``n`` is the
        number of nodes.

    kmax: int
       Maximum number of sample node pairs to use for approximation.

    sample_weight : float (default=1)
       Multiplicative factor for the number of sample node pairs used in approximation.
       Higher values may improve accuracy at the expense of increased computation time.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    nodes : dictionary
       Dictionary of nodes with betweenness centrality as the value.

    See Also
    --------
    current_flow_betweenness_centrality

    Notes
    -----
    The running time is $O((1/\epsilon^2)m{\sqrt k} \log n)$
    and the space required is $O(m)$ for $n$ nodes and $m$ edges.

    If the edges have a 'weight' attribute they will be used as
    weights in this algorithm.  Unspecified weights are set to 1.

    References
    ----------
    .. [1] Ulrik Brandes and Daniel Fleischer:
       Centrality Measures Based on Current Flow.
       Proc. 22nd Symp. Theoretical Aspects of Computer Science (STACS '05).
       LNCS 3404, pp. 533-544. Springer-Verlag, 2005.
       https://doi.org/10.1007/978-3-540-31856-9_44
    """
    import numpy as np

    if not nx.is_connected(G):
        raise nx.NetworkXError("Graph not connected.")

    n = G.number_of_nodes()

    # For small graphs (n < 3), betweenness centrality is always 0 for all nodes
    # since no node can be "between" any pair of other nodes
    if n < 3:
        return dict.fromkeys(G, 0.0)

    if epsilon <= 0:
        raise nx.NetworkXError(f"Epsilon must be positive. Got {epsilon=}.")

    if sample_weight <= 0:
        raise nx.NetworkXError(f"Sample weight must be positive. Got {sample_weight=}.")

    nb = (n - 1.0) * (n - 2.0)  # normalization factor
    cstar = n * (n - 1) / nb
    k = int(sample_weight * np.ceil((cstar / epsilon) ** 2 * np.log(n)))
    if k > kmax:
        msg = f"Number random pairs k>kmax ({k}>{kmax}) "
        raise nx.NetworkXError(msg, "Increase kmax or epsilon")

    solvername = {
        "full": FullInverseLaplacian,
        "lu": SuperLUInverseLaplacian,
        "cg": CGInverseLaplacian,
    }
    ordering = list(reverse_cuthill_mckee_ordering(G))
    # make a copy with integer labels according to rcm ordering
    # this could be done without a copy if we really wanted to
    H = nx.relabel_nodes(G, dict(zip(ordering, range(n))))
    L = nx.laplacian_matrix(H, nodelist=range(n), weight=weight).asformat("csc")
    L = L.astype(dtype)
    C = solvername[solver](L, dtype=dtype)  # initialize solver
    betweenness = dict.fromkeys(H, 0.0)
    cstar2k = cstar / (2 * k)
    for _ in range(k):
        s, t = pair = seed.sample(range(n), 2)
        b = np.zeros(n, dtype=dtype)
        b[s] = 1
        b[t] = -1
        p = C.solve(b)
        for v in H:
            if v in pair:
                continue
            for nbr in H[v]:
                w = H[v][nbr].get(weight, 1.0)
                betweenness[v] += float(w * np.abs(p[v] - p[nbr]) * cstar2k)
    if normalized:
        factor = 1.0
    else:
        factor = nb / 2.0
    # remap to original node names and "unnormalize" if required
    return {ordering[k]: v * factor for k, v in betweenness.items()}

