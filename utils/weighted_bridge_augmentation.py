
def weighted_bridge_augmentation(G, avail, weight=None):
    """Finds an approximate min-weight 2-edge-augmentation of G.

    This is an implementation of the approximation algorithm detailed in [1]_.
    It chooses a set of edges from avail to add to G that renders it
    2-edge-connected if such a subset exists.  This is done by finding a
    minimum spanning arborescence of a specially constructed metagraph.

    Parameters
    ----------
    G : NetworkX graph
       An undirected graph.

    avail : set of 2 or 3 tuples.
        candidate edges (with optional weights) to choose from

    weight : string
        key to use to find weights if avail is a set of 3-tuples where the
        third item in each tuple is a dictionary.

    Yields
    ------
    edge : tuple
        Edges in the subset of avail chosen to bridge augment G.

    Notes
    -----
    Finding a weighted 2-edge-augmentation is NP-hard.
    Any edge not in ``avail`` is considered to have a weight of infinity.
    The approximation factor is 2 if ``G`` is connected and 3 if it is not.
    Runs in :math:`O(m + n log(n))` time

    References
    ----------
    .. [1] Khuller, Samir, and Ramakrishna Thurimella. (1993) Approximation
        algorithms for graph augmentation.
        http://www.sciencedirect.com/science/article/pii/S0196677483710102

    See Also
    --------
    :func:`bridge_augmentation`
    :func:`k_edge_augmentation`

    Examples
    --------
    >>> G = nx.path_graph((1, 2, 3, 4))
    >>> # When the weights are equal, (1, 4) is the best
    >>> avail = [(1, 4, 1), (1, 3, 1), (2, 4, 1)]
    >>> sorted(weighted_bridge_augmentation(G, avail))
    [(1, 4)]
    >>> # Giving (1, 4) a high weight makes the two edge solution the best.
    >>> avail = [(1, 4, 1000), (1, 3, 1), (2, 4, 1)]
    >>> sorted(weighted_bridge_augmentation(G, avail))
    [(1, 3), (2, 4)]
    >>> # ------
    >>> G = nx.path_graph((1, 2, 3, 4))
    >>> G.add_node(5)
    >>> avail = [(1, 5, 11), (2, 5, 10), (4, 3, 1), (4, 5, 1)]
    >>> sorted(weighted_bridge_augmentation(G, avail=avail))
    [(1, 5), (4, 5)]
    >>> avail = [(1, 5, 11), (2, 5, 10), (4, 3, 1), (4, 5, 51)]
    >>> sorted(weighted_bridge_augmentation(G, avail=avail))
    [(1, 5), (2, 5), (4, 5)]
    """

    if weight is None:
        weight = "weight"

    # If input G is not connected the approximation factor increases to 3
    if not nx.is_connected(G):
        H = G.copy()
        connectors = list(one_edge_augmentation(H, avail=avail, weight=weight))
        H.add_edges_from(connectors)

        yield from connectors
    else:
        connectors = []
        H = G

    if len(avail) == 0:
        if nx.has_bridges(H):
            raise nx.NetworkXUnfeasible("no augmentation possible")

    avail_uv, avail_w = _unpack_available_edges(avail, weight=weight, G=H)

    # Collapse input into a metagraph. Meta nodes are bridge-ccs
    bridge_ccs = nx.connectivity.bridge_components(H)
    C = collapse(H, bridge_ccs)

    # Use the meta graph to shrink avail to a small feasible subset
    mapping = C.graph["mapping"]
    # Choose the minimum weight feasible edge in each group
    meta_to_wuv = {
        (mu, mv): (w, uv)
        for (mu, mv), uv, w in _lightest_meta_edges(mapping, avail_uv, avail_w)
    }

    # Mapping of terms from (Khuller and Thurimella):
    #     C         : G_0 = (V, E^0)
    #        This is the metagraph where each node is a 2-edge-cc in G.
    #        The edges in C represent bridges in the original graph.
    #     (mu, mv)  : E - E^0  # they group both avail and given edges in E
    #     T         : \Gamma
    #     D         : G^D = (V, E_D)

    #     The paper uses ancestor because children point to parents, which is
    #     contrary to networkx standards.  So, we actually need to run
    #     nx.least_common_ancestor on the reversed Tree.

    # Pick an arbitrary leaf from C as the root
    try:
        root = next(n for n, d in C.degree() if d == 1)
    except StopIteration:  # no nodes found with degree == 1
        return
    # Root C into a tree TR by directing all edges away from the root
    # Note in their paper T directs edges towards the root
    TR = nx.dfs_tree(C, root)

    # Add to D the directed edges of T and set their weight to zero
    # This indicates that it costs nothing to use edges that were given.
    D = nx.reverse(TR).copy()

    nx.set_edge_attributes(D, name="weight", values=0)

    # The LCA of mu and mv in T is the shared ancestor of mu and mv that is
    # located farthest from the root.
    lca_gen = nx.tree_all_pairs_lowest_common_ancestor(
        TR, root=root, pairs=meta_to_wuv.keys()
    )

    for (mu, mv), lca in lca_gen:
        w, uv = meta_to_wuv[(mu, mv)]
        if lca == mu:
            # If u is an ancestor of v in TR, then add edge u->v to D
            D.add_edge(lca, mv, weight=w, generator=uv)
        elif lca == mv:
            # If v is an ancestor of u in TR, then add edge v->u to D
            D.add_edge(lca, mu, weight=w, generator=uv)
        else:
            # If neither u nor v is a ancestor of the other in TR
            # let t = lca(TR, u, v) and add edges t->u and t->v
            # Track the original edge that GENERATED these edges.
            D.add_edge(lca, mu, weight=w, generator=uv)
            D.add_edge(lca, mv, weight=w, generator=uv)

    # Then compute a minimum rooted branching
    try:
        # Note the original edges must be directed towards to root for the
        # branching to give us a bridge-augmentation.
        A = _minimum_rooted_branching(D, root)
    except nx.NetworkXException as err:
        # If there is no branching then augmentation is not possible
        raise nx.NetworkXUnfeasible("no 2-edge-augmentation possible") from err

    # For each edge e, in the branching that did not belong to the directed
    # tree T, add the corresponding edge that **GENERATED** it (this is not
    # necessarily e itself!)

    # ensure the third case does not generate edges twice
    bridge_connectors = set()
    for mu, mv in A.edges():
        data = D.get_edge_data(mu, mv)
        if "generator" in data:
            # Add the avail edge that generated the branching edge.
            edge = data["generator"]
            bridge_connectors.add(edge)

    yield from bridge_connectors

