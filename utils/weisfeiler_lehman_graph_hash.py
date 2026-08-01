
def weisfeiler_lehman_graph_hash(
    G, edge_attr=None, node_attr=None, iterations=3, digest_size=16
):
    """Return Weisfeiler Lehman (WL) graph hash.

    .. Warning:: Hash values for directed graphs and graphs without edge or
        node attributes have changed in v3.5. In previous versions,
        directed graphs did not distinguish in- and outgoing edges. Also,
        graphs without attributes set initial states such that effectively
        one extra iteration of WL occurred than indicated by `iterations`.
        For undirected graphs without node or edge labels, the old
        hashes can be obtained by increasing the iteration count by one.
        For more details, see `issue #7806
        <https://github.com/networkx/networkx/issues/7806>`_.

    The function iteratively aggregates and hashes neighborhoods of each node.
    After each node's neighbors are hashed to obtain updated node labels,
    a hashed histogram of resulting labels is returned as the final hash.

    Hashes are identical for isomorphic graphs and strong guarantees that
    non-isomorphic graphs will get different hashes. See [1]_ for details.

    If no node or edge attributes are provided, the degree of each node
    is used as its initial label.
    Otherwise, node and/or edge labels are used to compute the hash.

    Parameters
    ----------
    G : graph
        The graph to be hashed.
        Can have node and/or edge attributes. Can also have no attributes.
    edge_attr : string, optional (default=None)
        The key in edge attribute dictionary to be used for hashing.
        If None, edge labels are ignored.
    node_attr: string, optional (default=None)
        The key in node attribute dictionary to be used for hashing.
        If None, and no edge_attr given, use the degrees of the nodes as labels.
    iterations: int, optional (default=3)
        Number of neighbor aggregations to perform.
        Should be larger for larger graphs.
    digest_size: int, optional (default=16)
        Size (in bytes) of blake2b hash digest to use for hashing node labels.

    Returns
    -------
    h : string
        Hexadecimal string corresponding to hash of `G` (length ``2 * digest_size``).

    Raises
    ------
    ValueError
        If `iterations` is not a positve number.

    Examples
    --------
    Two graphs with edge attributes that are isomorphic, except for
    differences in the edge labels.

    >>> G1 = nx.Graph()
    >>> G1.add_edges_from(
    ...     [
    ...         (1, 2, {"label": "A"}),
    ...         (2, 3, {"label": "A"}),
    ...         (3, 1, {"label": "A"}),
    ...         (1, 4, {"label": "B"}),
    ...     ]
    ... )
    >>> G2 = nx.Graph()
    >>> G2.add_edges_from(
    ...     [
    ...         (5, 6, {"label": "B"}),
    ...         (6, 7, {"label": "A"}),
    ...         (7, 5, {"label": "A"}),
    ...         (7, 8, {"label": "A"}),
    ...     ]
    ... )

    Omitting the `edge_attr` option, results in identical hashes.

    >>> nx.weisfeiler_lehman_graph_hash(G1)
    'c045439172215f49e0bef8c3d26c6b61'
    >>> nx.weisfeiler_lehman_graph_hash(G2)
    'c045439172215f49e0bef8c3d26c6b61'

    With edge labels, the graphs are no longer assigned
    the same hash digest.

    >>> nx.weisfeiler_lehman_graph_hash(G1, edge_attr="label")
    'c653d85538bcf041d88c011f4f905f10'
    >>> nx.weisfeiler_lehman_graph_hash(G2, edge_attr="label")
    '3dcd84af1ca855d0eff3c978d88e7ec7'

    Notes
    -----
    To return the WL hashes of each subgraph of a graph, use
    `weisfeiler_lehman_subgraph_hashes`

    Similarity between hashes does not imply similarity between graphs.

    References
    ----------
    .. [1] Shervashidze, Nino, Pascal Schweitzer, Erik Jan Van Leeuwen,
       Kurt Mehlhorn, and Karsten M. Borgwardt. Weisfeiler Lehman
       Graph Kernels. Journal of Machine Learning Research. 2011.
       http://www.jmlr.org/papers/volume12/shervashidze11a/shervashidze11a.pdf

    See also
    --------
    weisfeiler_lehman_subgraph_hashes
    """

    if G.is_directed():
        _neighborhood_aggregate = _neighborhood_aggregate_directed
        warnings.warn(
            "The hashes produced for directed graphs changed in version v3.5"
            " due to a bugfix to track in and out edges separately (see documentation).",
            UserWarning,
            stacklevel=2,
        )
    else:
        _neighborhood_aggregate = _neighborhood_aggregate_undirected

    def weisfeiler_lehman_step(G, labels, edge_attr=None):
        """
        Apply neighborhood aggregation to each node
        in the graph.
        Computes a dictionary with labels for each node.
        """
        new_labels = {}
        for node in G.nodes():
            label = _neighborhood_aggregate(G, node, labels, edge_attr=edge_attr)
            new_labels[node] = _hash_label(label, digest_size)
        return new_labels

    if iterations <= 0:
        raise ValueError("The WL algorithm requires that `iterations` be positive")

    # set initial node labels
    node_labels = _init_node_labels(G, edge_attr, node_attr)

    # If the graph has no attributes, initial labels are the nodes' degrees.
    # This is equivalent to doing the first iterations of WL.
    if not edge_attr and not node_attr:
        iterations -= 1

    subgraph_hash_counts = []
    for _ in range(iterations):
        node_labels = weisfeiler_lehman_step(G, node_labels, edge_attr=edge_attr)
        counter = Counter(node_labels.values())
        # sort the counter, extend total counts
        subgraph_hash_counts.extend(sorted(counter.items(), key=lambda x: x[0]))

    # hash the final counter
    return _hash_label(str(tuple(subgraph_hash_counts)), digest_size)

