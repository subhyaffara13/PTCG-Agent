
def directed_laplacian_matrix(
    G, nodelist=None, weight="weight", walk_type=None, alpha=0.95
):
    r"""Returns the directed Laplacian matrix of G.

    The graph directed Laplacian is the matrix

    .. math::

        L = I - \frac{1}{2} \left (\Phi^{1/2} P \Phi^{-1/2} + \Phi^{-1/2} P^T \Phi^{1/2} \right )

    where `I` is the identity matrix, `P` is the transition matrix of the
    graph, and `\Phi` a matrix with the Perron vector of `P` in the diagonal and
    zeros elsewhere [1]_.

    Depending on the value of walk_type, `P` can be the transition matrix
    induced by a random walk, a lazy random walk, or a random walk with
    teleportation (PageRank).

    Parameters
    ----------
    G : DiGraph
       A NetworkX graph

    nodelist : list, optional
       The rows and columns are ordered according to the nodes in nodelist.
       If nodelist is None, then the ordering is produced by G.nodes().

    weight : string or None, optional (default='weight')
       The edge data key used to compute each value in the matrix.
       If None, then each edge has weight 1.

    walk_type : string or None, optional (default=None)
       One of ``"random"``, ``"lazy"``, or ``"pagerank"``. If ``walk_type=None``
       (the default), then a value is selected according to the properties of `G`:
       - ``walk_type="random"`` if `G` is strongly connected and aperiodic
       - ``walk_type="lazy"`` if `G` is strongly connected but not aperiodic
       - ``walk_type="pagerank"`` for all other cases.

    alpha : real
       (1 - alpha) is the teleportation probability used with pagerank

    Returns
    -------
    L : NumPy matrix
      Normalized Laplacian of G.

    Notes
    -----
    Only implemented for DiGraphs

    The result is always a symmetric matrix.

    This calculation uses the out-degree of the graph `G`. To use the
    in-degree for calculations instead, use `G.reverse(copy=False)` and
    take the transpose.

    See Also
    --------
    laplacian_matrix
    normalized_laplacian_matrix
    directed_combinatorial_laplacian_matrix

    References
    ----------
    .. [1] Fan Chung (2005).
       Laplacians and the Cheeger inequality for directed graphs.
       Annals of Combinatorics, 9(1), 2005
    """
    import numpy as np
    import scipy as sp

    # NOTE: P has type ndarray if walk_type=="pagerank", else csr_array
    P = _transition_matrix(
        G, nodelist=nodelist, weight=weight, walk_type=walk_type, alpha=alpha
    )

    n, m = P.shape

    evals, evecs = sp.sparse.linalg.eigs(P.T, k=1)
    v = evecs.flatten().real
    p = v / v.sum()
    # p>=0 by Perron-Frobenius Thm. Use abs() to fix roundoff across zero gh-6865
    sqrtp = np.sqrt(np.abs(p))
    Q = (
        sp.sparse.dia_array((sqrtp, 0), shape=(n, n)).tocsr()
        @ P
        @ sp.sparse.dia_array((1.0 / sqrtp, 0), shape=(n, n)).tocsr()
    )
    # NOTE: This could be sparsified for the non-pagerank cases
    I = np.identity(len(G))

    return I - (Q + Q.T) / 2.0

