
def normalized_laplacian_matrix(G, nodelist=None, weight="weight"):
    r"""Returns the normalized Laplacian matrix of G.

    The normalized graph Laplacian is the matrix

    .. math::

        N = D^{-1/2} L D^{-1/2}

    where `L` is the graph Laplacian and `D` is the diagonal matrix of
    node degrees [1]_.

    Parameters
    ----------
    G : graph
       A NetworkX graph

    nodelist : list, optional
       The rows and columns are ordered according to the nodes in nodelist.
       If nodelist is None, then the ordering is produced by G.nodes().

    weight : string or None, optional (default='weight')
       The edge data key used to compute each value in the matrix.
       If None, then each edge has weight 1.

    Returns
    -------
    N : SciPy sparse array
      The normalized Laplacian matrix of G.

    Notes
    -----
    For MultiGraph, the edges weights are summed.
    See :func:`to_numpy_array` for other options.

    If the Graph contains selfloops, D is defined as ``diag(sum(A, 1))``, where A is
    the adjacency matrix [2]_.

    This calculation uses the out-degree of the graph `G`. To use the
    in-degree for calculations instead, use `G.reverse(copy=False)` and
    take the transpose.

    For an unnormalized output, use `laplacian_matrix`.

    Examples
    --------

    >>> import numpy as np
    >>> edges = [
    ...     (1, 2),
    ...     (2, 1),
    ...     (2, 4),
    ...     (4, 3),
    ...     (3, 4),
    ... ]
    >>> DiG = nx.DiGraph(edges)
    >>> print(nx.normalized_laplacian_matrix(DiG).toarray())
    [[ 1.         -0.70710678  0.          0.        ]
     [-0.70710678  1.         -0.70710678  0.        ]
     [ 0.          0.          1.         -1.        ]
     [ 0.          0.         -1.          1.        ]]

    Notice that node 4 is represented by the third column and row. This is because
    by default the row/column order is the order of `G.nodes` (i.e. the node added
    order -- in the edgelist, 4 first appears in (2, 4), before node 3 in edge (4, 3).)
    To control the node order of the matrix, use the `nodelist` argument.

    >>> print(nx.normalized_laplacian_matrix(DiG, nodelist=[1, 2, 3, 4]).toarray())
    [[ 1.         -0.70710678  0.          0.        ]
     [-0.70710678  1.          0.         -0.70710678]
     [ 0.          0.          1.         -1.        ]
     [ 0.          0.         -1.          1.        ]]
    >>> G = nx.Graph(edges)
    >>> print(nx.normalized_laplacian_matrix(G).toarray())
    [[ 1.         -0.70710678  0.          0.        ]
     [-0.70710678  1.         -0.5         0.        ]
     [ 0.         -0.5         1.         -0.70710678]
     [ 0.          0.         -0.70710678  1.        ]]

    See Also
    --------
    laplacian_matrix
    normalized_laplacian_spectrum
    directed_laplacian_matrix
    directed_combinatorial_laplacian_matrix

    References
    ----------
    .. [1] Fan Chung-Graham, Spectral Graph Theory,
       CBMS Regional Conference Series in Mathematics, Number 92, 1997.
    .. [2] Steve Butler, Interlacing For Weighted Graphs Using The Normalized
       Laplacian, Electronic Journal of Linear Algebra, Volume 16, pp. 90-98,
       March 2007.
    .. [3] Langville, Amy N., and Carl D. Meyer. Google’s PageRank and Beyond:
       The Science of Search Engine Rankings. Princeton University Press, 2006.
    """
    import numpy as np
    import scipy as sp

    if nodelist is None:
        nodelist = list(G)
    A = nx.to_scipy_sparse_array(G, nodelist=nodelist, weight=weight, format="csr")
    n, _ = A.shape
    diags = A.sum(axis=1)
    D = sp.sparse.dia_array((diags, 0), shape=(n, n)).tocsr()
    L = D - A
    with np.errstate(divide="ignore"):
        diags_sqrt = 1.0 / np.sqrt(diags)
    diags_sqrt[np.isinf(diags_sqrt)] = 0
    DH = sp.sparse.dia_array((diags_sqrt, 0), shape=(n, n)).tocsr()
    return DH @ (L @ DH)

