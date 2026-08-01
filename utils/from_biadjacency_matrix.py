
def from_biadjacency_matrix(
    A,
    create_using=None,
    edge_attribute="weight",
    *,
    row_order=None,
    column_order=None,
):
    r"""Creates a new bipartite graph from a biadjacency matrix given as a
    SciPy sparse array.

    Parameters
    ----------
    A : scipy sparse array
      A biadjacency matrix representation of a graph

    create_using : NetworkX graph
       Use specified graph for result.  The default is Graph()

    edge_attribute : string
       Name of edge attribute to store matrix numeric value. The data will
       have the same type as the matrix entry (int, float, (real,imag)).

    row_order : list, optional (default: range(number of rows in `A`))
        A list of the nodes represented by the rows of the matrix `A`. Will
        be represented in the graph as nodes with the `bipartite` attribute set
        to 0. Must be the same length as the number of rows in `A`.

    column_order : list, optional (default: range(number of columns in `A`))
        A list of the nodes represented by the columns of the matrix `A`. Will
        be represented in the graph as nodes with the `bipartite` attribute set
        to 1. Must be the same length as the number of columns in `A`.

    Returns
    -------
    G : NetworkX graph
        A bipartite graph with edges from the biadjacency matrix `A`, and
        nodes from `row_order` and `column_order`.

    Raises
    ------
    ValueError
        If `row_order` or `column_order` are provided and are not the same
        length as the number of rows or columns in `A`, respectively.

    Notes
    -----
    The nodes are labeled with the attribute `bipartite` set to an integer
    0 or 1 representing membership in the `top` set (`bipartite=0`) or `bottom`
    set (`bipartite=1`) of the bipartite graph.

    If `create_using` is an instance of :class:`networkx.MultiGraph` or
    :class:`networkx.MultiDiGraph` and the entries of `A` are of
    type :class:`int`, then this function returns a multigraph (of the same
    type as `create_using`) with parallel edges. In this case, `edge_attribute`
    will be ignored.

    See Also
    --------
    biadjacency_matrix
    from_numpy_array

    References
    ----------
    [1] https://en.wikipedia.org/wiki/Adjacency_matrix#Adjacency_matrix_of_a_bipartite_graph
    """
    G = nx.empty_graph(0, create_using)
    n, m = A.shape
    # Check/set row_order and column_order to have correct length and default values
    row_order, column_order = _validate_initialize_bipartite_nodelists(
        A, row_order, column_order
    )

    # Make sure we get even the isolated nodes of the graph.
    G.add_nodes_from(range(n), bipartite=0)
    G.add_nodes_from(range(n, n + m), bipartite=1)
    # Create an iterable over (u, v, w) triples and for each triple, add an
    # edge from u to v with weight w.
    triples = ((u, n + v, d) for (u, v, d) in _generate_weighted_edges(A))
    # If the entries in the adjacency matrix are integers and the graph is a
    # multigraph, then create parallel edges, each with weight 1, for each
    # entry in the adjacency matrix. Otherwise, create one edge for each
    # positive entry in the adjacency matrix and set the weight of that edge to
    # be the entry in the matrix.
    if A.dtype.kind in ("i", "u") and G.is_multigraph():
        chain = itertools.chain.from_iterable
        triples = chain(((u, v, 1) for d in range(w)) for (u, v, w) in triples)
    G.add_weighted_edges_from(triples, weight=edge_attribute)

    # If the user provided nodelists, relabel the nodes of the graph inplace
    mapping = dict(
        itertools.chain(zip(range(n), row_order), zip(range(n, n + m), column_order))
    )
    if len(mapping):
        nx.relabel_nodes(G, mapping, copy=False)
    return G

