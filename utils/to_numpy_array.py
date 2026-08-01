
def to_numpy_array(
    G,
    nodelist=None,
    dtype=None,
    order=None,
    multigraph_weight=sum,
    weight="weight",
    nonedge=0.0,
):
    """Returns the graph adjacency matrix as a NumPy array.

    Parameters
    ----------
    G : graph
        The NetworkX graph used to construct the NumPy array.

    nodelist : list, optional
        The rows and columns are ordered according to the nodes in `nodelist`.
        If `nodelist` is ``None``, then the ordering is produced by ``G.nodes()``.

    dtype : NumPy data type, optional
        A NumPy data type used to initialize the array. If None, then the NumPy
        default is used. The dtype can be structured if `weight=None`, in which
        case the dtype field names are used to look up edge attributes. The
        result is a structured array where each named field in the dtype
        corresponds to the adjacency for that edge attribute. See examples for
        details.

    order : {'C', 'F'}, optional
        Whether to store multidimensional data in C- or Fortran-contiguous
        (row- or column-wise) order in memory. If None, then the NumPy default
        is used.

    multigraph_weight : callable, optional
        An function that determines how weights in multigraphs are handled.
        The function should accept a sequence of weights and return a single
        value. The default is to sum the weights of the multiple edges.

    weight : string or None optional (default = 'weight')
        The edge attribute that holds the numerical value used for
        the edge weight. If an edge does not have that attribute, then the
        value 1 is used instead. `weight` must be ``None`` if a structured
        dtype is used.

    nonedge : array_like (default = 0.0)
        The value used to represent non-edges in the adjacency matrix.
        The array values corresponding to nonedges are typically set to zero.
        However, this could be undesirable if there are array values
        corresponding to actual edges that also have the value zero. If so,
        one might prefer nonedges to have some other value, such as ``nan``.

    Returns
    -------
    A : NumPy ndarray
        Graph adjacency matrix

    Raises
    ------
    NetworkXError
        If `dtype` is a structured dtype and `G` is a multigraph
    ValueError
        If `dtype` is a structured dtype and `weight` is not `None`

    See Also
    --------
    from_numpy_array

    Notes
    -----
    For directed graphs, entry ``i, j`` corresponds to an edge from ``i`` to ``j``.

    Entries in the adjacency matrix are given by the `weight` edge attribute.
    When an edge does not have a weight attribute, the value of the entry is
    set to the number 1.  For multiple (parallel) edges, the values of the
    entries are determined by the `multigraph_weight` parameter. The default is
    to sum the weight attributes for each of the parallel edges.

    When `nodelist` does not contain every node in `G`, the adjacency matrix is
    built from the subgraph of `G` that is induced by the nodes in `nodelist`.

    The convention used for self-loop edges in graphs is to assign the
    diagonal array entry value to the weight attribute of the edge
    (or the number 1 if the edge has no weight attribute). If the
    alternate convention of doubling the edge weight is desired the
    resulting NumPy array can be modified as follows:

    >>> import numpy as np
    >>> G = nx.Graph([(1, 1)])
    >>> A = nx.to_numpy_array(G)
    >>> A
    array([[1.]])
    >>> A[np.diag_indices_from(A)] *= 2
    >>> A
    array([[2.]])

    Examples
    --------
    >>> G = nx.MultiDiGraph()
    >>> G.add_edge(0, 1, weight=2)
    0
    >>> G.add_edge(1, 0)
    0
    >>> G.add_edge(2, 2, weight=3)
    0
    >>> G.add_edge(2, 2)
    1
    >>> nx.to_numpy_array(G, nodelist=[0, 1, 2])
    array([[0., 2., 0.],
           [1., 0., 0.],
           [0., 0., 4.]])

    When `nodelist` argument is used, nodes of `G` which do not appear in the `nodelist`
    and their edges are not included in the adjacency matrix. Here is an example:

    >>> G = nx.Graph()
    >>> G.add_edge(3, 1)
    >>> G.add_edge(2, 0)
    >>> G.add_edge(2, 1)
    >>> G.add_edge(3, 0)
    >>> nx.to_numpy_array(G, nodelist=[1, 2, 3])
    array([[0., 1., 1.],
           [1., 0., 0.],
           [1., 0., 0.]])

    This function can also be used to create adjacency matrices for multiple
    edge attributes with structured dtypes:

    >>> G = nx.Graph()
    >>> G.add_edge(0, 1, weight=10)
    >>> G.add_edge(1, 2, cost=5)
    >>> G.add_edge(2, 3, weight=3, cost=-4.0)
    >>> dtype = np.dtype([("weight", int), ("cost", float)])
    >>> A = nx.to_numpy_array(G, dtype=dtype, weight=None)
    >>> A["weight"]
    array([[ 0, 10,  0,  0],
           [10,  0,  1,  0],
           [ 0,  1,  0,  3],
           [ 0,  0,  3,  0]])
    >>> A["cost"]
    array([[ 0.,  1.,  0.,  0.],
           [ 1.,  0.,  5.,  0.],
           [ 0.,  5.,  0., -4.],
           [ 0.,  0., -4.,  0.]])

    As stated above, the argument "nonedge" is useful especially when there are
    actually edges with weight 0 in the graph. Setting a nonedge value different than 0,
    makes it much clearer to differentiate such 0-weighted edges and actual nonedge values.

    >>> G = nx.Graph()
    >>> G.add_edge(3, 1, weight=2)
    >>> G.add_edge(2, 0, weight=0)
    >>> G.add_edge(2, 1, weight=0)
    >>> G.add_edge(3, 0, weight=1)
    >>> nx.to_numpy_array(G, nonedge=-1.0)
    array([[-1.,  2., -1.,  1.],
           [ 2., -1.,  0., -1.],
           [-1.,  0., -1.,  0.],
           [ 1., -1.,  0., -1.]])
    """
    import numpy as np

    if nodelist is None:
        nodelist = list(G)
    nlen = len(nodelist)

    # Input validation
    nodeset = set(nodelist)
    if nodeset - set(G):
        raise nx.NetworkXError(f"Nodes {nodeset - set(G)} in nodelist is not in G")
    if len(nodeset) < nlen:
        raise nx.NetworkXError("nodelist contains duplicates.")

    A = np.full((nlen, nlen), fill_value=nonedge, dtype=dtype, order=order)

    # Corner cases: empty nodelist or graph without any edges
    if nlen == 0 or G.number_of_edges() == 0:
        return A

    # If dtype is structured and weight is None, use dtype field names as
    # edge attributes
    edge_attrs = None  # Only single edge attribute by default
    if A.dtype.names:
        if weight is None:
            edge_attrs = dtype.names
        else:
            raise ValueError(
                "Specifying `weight` not supported for structured dtypes\n."
                "To create adjacency matrices from structured dtypes, use `weight=None`."
            )

    # Map nodes to row/col in matrix
    idx = dict(zip(nodelist, range(nlen)))
    if len(nodelist) < len(G):
        G = G.subgraph(nodelist).copy()

    # Collect all edge weights and reduce with `multigraph_weights`
    if G.is_multigraph():
        if edge_attrs:
            raise nx.NetworkXError(
                "Structured arrays are not supported for MultiGraphs"
            )
        d = defaultdict(list)
        for u, v, wt in G.edges(data=weight, default=1.0):
            d[(idx[u], idx[v])].append(wt)
        i, j = np.array(list(d.keys())).T  # indices
        wts = [multigraph_weight(ws) for ws in d.values()]  # reduced weights
    else:
        i, j, wts = [], [], []

        # Special branch: multi-attr adjacency from structured dtypes
        if edge_attrs:
            # Extract edges with all data
            for u, v, data in G.edges(data=True):
                i.append(idx[u])
                j.append(idx[v])
                wts.append(data)
            # Map each attribute to the appropriate named field in the
            # structured dtype
            for attr in edge_attrs:
                attr_data = [wt.get(attr, 1.0) for wt in wts]
                A[attr][i, j] = attr_data
                if not G.is_directed():
                    A[attr][j, i] = attr_data
            return A

        for u, v, wt in G.edges(data=weight, default=1.0):
            i.append(idx[u])
            j.append(idx[v])
            wts.append(wt)

    # Set array values with advanced indexing
    A[i, j] = wts
    if not G.is_directed():
        A[j, i] = wts

    return A


def to_numpy_array(img) -> np.ndarray:
    if not is_valid_image(img):
        raise ValueError(f"Invalid image type: {type(img)}")

    if is_vision_available() and isinstance(img, PIL.Image.Image):
        return np.array(img)
    return to_numpy(img)

