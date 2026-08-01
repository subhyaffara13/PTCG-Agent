
def degree_sequence_tree(deg_sequence, create_using=None):
    """Return a tree with the given degree sequence.

    Two conditions must be met for a degree sequence to be valid for a tree:

    1. The number of nodes must be one more than the number of edges.
    2. The degree sequence must be trivial or have only strictly positive
       node degrees.

    Parameters
    ----------
    degree_sequence : iterable
        Iterable of node degrees.

    create_using : NetworkX graph constructor, optional (default=nx.Graph)
        Graph type to create. If graph instance, then cleared before populated.

    Returns
    -------
    networkx.Graph
        A tree with the given degree sequence.

    Raises
    ------
    NetworkXError
        If the degree sequence is not valid for a tree.

        If `create_using` is directed.

    See Also
    --------
    random_degree_sequence_graph
    """
    deg_sequence = list(deg_sequence)
    valid, reason = nx.utils.is_valid_tree_degree_sequence(deg_sequence)
    if not valid:
        raise nx.NetworkXError(reason)

    G = nx.empty_graph(0, create_using)
    if G.is_directed():
        raise nx.NetworkXError("Directed Graph not supported")

    if deg_sequence == [0]:
        G.add_node(0)
        return G

    # Sort all degrees greater than 1 in decreasing order.
    #
    # TODO Does this need to be sorted in reverse order?
    deg = sorted((s for s in deg_sequence if s > 1), reverse=True)

    # make path graph as backbone
    n = len(deg) + 2
    nx.add_path(G, range(n))
    last = n

    # add the leaves
    for source in range(1, n - 1):
        nedges = deg.pop() - 2
        G.add_edges_from((source, target) for target in range(last, last + nedges))
        last += nedges
    return G

