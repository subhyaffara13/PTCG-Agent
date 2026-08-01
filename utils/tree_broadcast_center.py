
def tree_broadcast_center(G):
    """Return the broadcast center of a tree.

    The broadcast center of a graph `G` denotes the set of nodes having
    minimum broadcast time [1]_. This function implements a linear algorithm
    for determining the broadcast center of a tree with ``n`` nodes. As a
    by-product, it also determines the broadcast time from the broadcast center.

    Parameters
    ----------
    G : Graph
        The graph should be an undirected tree.

    Returns
    -------
    b_T, b_C : (int, set) tuple
        Minimum broadcast time of the broadcast center in `G`, set of nodes
        in the broadcast center.

    Raises
    ------
    NetworkXNotImplemented
        If `G` is directed or is a multigraph.

    NotATree
        If `G` is not a tree.

    References
    ----------
    .. [1] Slater, P.J., Cockayne, E.J., Hedetniemi, S.T,
       Information dissemination in trees. SIAM J.Comput. 10(4), 692–701 (1981)
    """
    # Assert that the graph G is a tree
    if not nx.is_tree(G):
        raise nx.NotATree("G is not a tree")
    # step 0
    if (n := len(G)) < 3:
        return n - 1, set(G)

    # step 1
    U = {node for node, deg in G.degree if deg == 1}
    values = {n: 0 for n in U}
    T = G.copy()
    T.remove_nodes_from(U)

    # step 2
    W = {node for node, deg in T.degree if deg == 1}
    values.update((w, G.degree[w] - 1) for w in W)

    # step 3
    while len(T) >= 2:
        # step 4
        w = min(W, key=values.get)
        v = next(T.neighbors(w))

        # step 5
        U.add(w)
        W.remove(w)
        T.remove_node(w)

        # step 6
        if T.degree(v) == 1:
            # update t(v)
            values.update({v: _get_max_broadcast_value(G, U, v, values)})
            W.add(v)

    # step 7
    v = nx.utils.arbitrary_element(T)
    b_T = _get_max_broadcast_value(G, U, v, values)
    return b_T, _get_broadcast_centers(G, v, values, b_T)

