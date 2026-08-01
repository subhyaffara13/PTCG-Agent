
def to_scipy_sparse_array(G, nodelist=None, dtype=None, weight="weight", format="csr"):
    """Returns the graph adjacency matrix as a SciPy sparse array.

    Parameters
    ----------
    G : graph
        The NetworkX graph used to construct the sparse array.

    nodelist : list, optional
       The rows and columns are ordered according to the nodes in `nodelist`.
       If `nodelist` is None, then the ordering is produced by ``G.nodes()``.

    dtype : NumPy data-type, optional
        A valid NumPy dtype used to initialize the array. If None, then the
        NumPy default is used.

    weight : string or None, optional (default='weight')
        The edge attribute that holds the numerical value used for
        the edge weight.  If None then all edge weights are 1.

    format : str in {'bsr', 'csr', 'csc', 'coo', 'lil', 'dia', 'dok'}
        The format of the sparse array to be returned (default 'csr').  For
        some algorithms different implementations of sparse arrays
        can perform better.  See [1]_ for details.

    Returns
    -------
    A : SciPy sparse array
       Graph adjacency matrix.

    Notes
    -----
    For directed graphs, matrix entry ``i, j`` corresponds to an edge from
    ``i`` to ``j``.

    The values of the adjacency matrix are populated using the edge attribute held in
    parameter `weight`. When an edge does not have that attribute, the
    value of the entry is 1.

    For multiple edges the matrix values are the sums of the edge weights.

    When `nodelist` does not contain every node in `G`, the adjacency matrix
    is built from the subgraph of `G` that is induced by the nodes in
    `nodelist`.

    The convention used for self-loop edges in graphs is to assign the
    diagonal matrix entry value to the weight attribute of the edge
    (or the number 1 if the edge has no weight attribute).  If the
    alternate convention of doubling the edge weight is desired the
    resulting array can be modified as follows::

        >>> G = nx.Graph([(1, 1)])
        >>> A = nx.to_scipy_sparse_array(G)
        >>> A.toarray()
        array([[1]])
        >>> A.setdiag(A.diagonal() * 2)
        >>> A.toarray()
        array([[2]])

    Examples
    --------

    Basic usage:

    >>> G = nx.path_graph(4)
    >>> A = nx.to_scipy_sparse_array(G)
    >>> A  # doctest: +SKIP
    <Compressed Sparse Row sparse array of dtype 'int64'
        with 6 stored elements and shape (4, 4)>

    >>> A.toarray()
    array([[0, 1, 0, 0],
           [1, 0, 1, 0],
           [0, 1, 0, 1],
           [0, 0, 1, 0]])

    .. note:: The `toarray` method is used in these examples to better visualize
       the adjacency matrix. For a dense representation of the adjaceny matrix,
       use `to_numpy_array` instead.

    Directed graphs:

    >>> G = nx.DiGraph([(0, 1), (1, 2), (2, 3)])
    >>> nx.to_scipy_sparse_array(G).toarray()
    array([[0, 1, 0, 0],
           [0, 0, 1, 0],
           [0, 0, 0, 1],
           [0, 0, 0, 0]])

    >>> H = G.reverse()
    >>> H.edges
    OutEdgeView([(1, 0), (2, 1), (3, 2)])
    >>> nx.to_scipy_sparse_array(H).toarray()
    array([[0, 0, 0, 0],
           [1, 0, 0, 0],
           [0, 1, 0, 0],
           [0, 0, 1, 0]])

    By default, the order of the rows/columns of the adjacency matrix is determined
    by the ordering of the nodes in `G`:

    >>> G = nx.Graph()
    >>> G.add_nodes_from([3, 5, 0, 1])
    >>> G.add_edges_from([(1, 3), (1, 5)])
    >>> nx.to_scipy_sparse_array(G).toarray()
    array([[0, 0, 0, 1],
           [0, 0, 0, 1],
           [0, 0, 0, 0],
           [1, 1, 0, 0]])

    The ordering of the rows can be changed with `nodelist`:

    >>> ordered = [0, 1, 3, 5]
    >>> nx.to_scipy_sparse_array(G, nodelist=ordered).toarray()
    array([[0, 0, 0, 0],
           [0, 0, 1, 1],
           [0, 1, 0, 0],
           [0, 1, 0, 0]])

    If `nodelist` contains a subset of the nodes in `G`, the adjacency matrix
    for the node-induced subgraph is produced:

    >>> nx.to_scipy_sparse_array(G, nodelist=[1, 3, 5]).toarray()
    array([[0, 1, 1],
           [1, 0, 0],
           [1, 0, 0]])

    The values of the adjacency matrix are drawn from the edge attribute
    specified by the `weight` parameter:

    >>> G = nx.path_graph(4)
    >>> nx.set_edge_attributes(
    ...     G, values={(0, 1): 1, (1, 2): 10, (2, 3): 2}, name="weight"
    ... )
    >>> nx.set_edge_attributes(
    ...     G, values={(0, 1): 50, (1, 2): 35, (2, 3): 10}, name="capacity"
    ... )
    >>> nx.to_scipy_sparse_array(G).toarray()  # Default weight="weight"
    array([[ 0,  1,  0,  0],
           [ 1,  0, 10,  0],
           [ 0, 10,  0,  2],
           [ 0,  0,  2,  0]])
    >>> nx.to_scipy_sparse_array(G, weight="capacity").toarray()
    array([[ 0, 50,  0,  0],
           [50,  0, 35,  0],
           [ 0, 35,  0, 10],
           [ 0,  0, 10,  0]])

    Any edges that don't have a `weight` attribute default to 1:

    >>> G[1][2].pop("capacity")
    35
    >>> nx.to_scipy_sparse_array(G, weight="capacity").toarray()
    array([[ 0, 50,  0,  0],
           [50,  0,  1,  0],
           [ 0,  1,  0, 10],
           [ 0,  0, 10,  0]])

    When `G` is a multigraph, the values in the adjacency matrix are given by
    the sum of the `weight` edge attribute over each edge key:

    >>> G = nx.MultiDiGraph([(0, 1), (0, 1), (0, 1), (2, 0)])
    >>> nx.to_scipy_sparse_array(G).toarray()
    array([[0, 3, 0],
           [0, 0, 0],
           [1, 0, 0]])

    References
    ----------
    .. [1] Scipy Dev. References, "Sparse Arrays",
       https://docs.scipy.org/doc/scipy/reference/sparse.html
    """
    import scipy as sp

    if len(G) == 0:
        raise nx.NetworkXError("Graph has no nodes or edges")

    if nodelist is None:
        nodelist = list(G)
        nlen = len(G)
    else:
        nlen = len(nodelist)
        if nlen == 0:
            raise nx.NetworkXError("nodelist has no nodes")
        nodeset = set(G.nbunch_iter(nodelist))
        if nlen != len(nodeset):
            for n in nodelist:
                if n not in G:
                    raise nx.NetworkXError(f"Node {n} in nodelist is not in G")
            raise nx.NetworkXError("nodelist contains duplicates.")
        if nlen < len(G):
            G = G.subgraph(nodelist)

    index = dict(zip(nodelist, range(nlen)))
    coefficients = zip(
        *((index[u], index[v], wt) for u, v, wt in G.edges(data=weight, default=1))
    )
    try:
        row, col, data = coefficients
    except ValueError:
        # there is no edge in the subgraph
        row, col, data = [], [], []

    if G.is_directed():
        A = sp.sparse.coo_array((data, (row, col)), shape=(nlen, nlen), dtype=dtype)
    else:
        # symmetrize matrix
        d = data + data
        r = row + col
        c = col + row
        # selfloop entries get double counted when symmetrizing
        # so we subtract the data on the diagonal
        selfloops = list(nx.selfloop_edges(G, data=weight, default=1))
        if selfloops:
            diag_index, diag_data = zip(*((index[u], -wt) for u, v, wt in selfloops))
            d += diag_data
            r += diag_index
            c += diag_index
        A = sp.sparse.coo_array((d, (r, c)), shape=(nlen, nlen), dtype=dtype)
    try:
        return A.asformat(format)
    except ValueError as err:
        raise nx.NetworkXError(f"Unknown sparse matrix format: {format}") from err

