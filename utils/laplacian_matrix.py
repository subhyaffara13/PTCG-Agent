
def laplacian_matrix(G, nodelist=None, weight="weight"):
    """Returns the Laplacian matrix of G.

    The graph Laplacian is the matrix L = D - A, where
    A is the adjacency matrix and D is the diagonal matrix of node degrees.

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
    L : SciPy sparse array
      The Laplacian matrix of G.

    Notes
    -----
    For MultiGraph, the edges weights are summed.

    This returns an unnormalized matrix. For a normalized output,
    use `normalized_laplacian_matrix`, `directed_laplacian_matrix`,
    or `directed_combinatorial_laplacian_matrix`.

    This calculation uses the out-degree of the graph `G`. To use the
    in-degree for calculations instead, use `G.reverse(copy=False)` and
    take the transpose.

    See Also
    --------
    :func:`~networkx.convert_matrix.to_numpy_array`
    normalized_laplacian_matrix
    directed_laplacian_matrix
    directed_combinatorial_laplacian_matrix
    :func:`~networkx.linalg.spectrum.laplacian_spectrum`

    Examples
    --------
    For graphs with multiple connected components, L is permutation-similar
    to a block diagonal matrix where each block is the respective Laplacian
    matrix for each component.

    >>> G = nx.Graph([(1, 2), (2, 3), (4, 5)])
    >>> print(nx.laplacian_matrix(G).toarray())
    [[ 1 -1  0  0  0]
     [-1  2 -1  0  0]
     [ 0 -1  1  0  0]
     [ 0  0  0  1 -1]
     [ 0  0  0 -1  1]]

    >>> edges = [
    ...     (1, 2),
    ...     (2, 1),
    ...     (2, 4),
    ...     (4, 3),
    ...     (3, 4),
    ... ]
    >>> DiG = nx.DiGraph(edges)
    >>> print(nx.laplacian_matrix(DiG).toarray())
    [[ 1 -1  0  0]
     [-1  2 -1  0]
     [ 0  0  1 -1]
     [ 0  0 -1  1]]

    Notice that node 4 is represented by the third column and row. This is because
    by default the row/column order is the order of `G.nodes` (i.e. the node added
    order -- in the edgelist, 4 first appears in (2, 4), before node 3 in edge (4, 3).)
    To control the node order of the matrix, use the `nodelist` argument.

    >>> print(nx.laplacian_matrix(DiG, nodelist=[1, 2, 3, 4]).toarray())
    [[ 1 -1  0  0]
     [-1  2  0 -1]
     [ 0  0  1 -1]
     [ 0  0 -1  1]]

    This calculation uses the out-degree of the graph `G`. To use the
    in-degree for calculations instead, use `G.reverse(copy=False)` and
    take the transpose.

    >>> print(nx.laplacian_matrix(DiG.reverse(copy=False)).toarray().T)
    [[ 1 -1  0  0]
     [-1  1 -1  0]
     [ 0  0  2 -1]
     [ 0  0 -1  1]]

    References
    ----------
    .. [1] Langville, Amy N., and Carl D. Meyer. Google’s PageRank and Beyond:
       The Science of Search Engine Rankings. Princeton University Press, 2006.

    """
    import scipy as sp

    if nodelist is None:
        nodelist = list(G)
    A = nx.to_scipy_sparse_array(G, nodelist=nodelist, weight=weight, format="csr")
    n, m = A.shape
    D = sp.sparse.dia_array((A.sum(axis=1), 0), shape=(m, n)).tocsr()
    return D - A

