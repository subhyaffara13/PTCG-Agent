
def unconstrained_one_edge_augmentation(G):
    """Finds the smallest set of edges to connect G.

    This is a variant of the unweighted MST problem.
    If G is not empty, a feasible solution always exists.

    Parameters
    ----------
    G : NetworkX graph
       An undirected graph.

    Yields
    ------
    edge : tuple
        Edges in the one-edge-augmentation of G

    See Also
    --------
    :func:`one_edge_augmentation`
    :func:`k_edge_augmentation`

    Examples
    --------
    >>> G = nx.Graph([(1, 2), (2, 3), (4, 5)])
    >>> G.add_nodes_from([6, 7, 8])
    >>> sorted(unconstrained_one_edge_augmentation(G))
    [(1, 4), (4, 6), (6, 7), (7, 8)]
    """
    ccs1 = list(nx.connected_components(G))
    C = collapse(G, ccs1)
    # When we are not constrained, we can just make a meta graph tree.
    meta_nodes = list(C.nodes())
    # build a path in the metagraph
    meta_aug = list(zip(meta_nodes, meta_nodes[1:]))
    # map that path to the original graph
    inverse = defaultdict(list)
    for k, v in C.graph["mapping"].items():
        inverse[v].append(k)
    for mu, mv in meta_aug:
        yield (inverse[mu][0], inverse[mv][0])

