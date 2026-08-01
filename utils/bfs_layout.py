
def bfs_layout(G, start, *, align="vertical", scale=1, center=None, store_pos_as=None):
    """Position nodes according to breadth-first search algorithm.

    Parameters
    ----------
    G : NetworkX graph
        A position will be assigned to every node in G.

    start : node in `G`
        Starting node for bfs

    align : string (default='vertical')
        The alignment of nodes within a layer, either `"vertical"` or
        `"horizontal"`.

    scale : number (default: 1)
        Scale factor for positions.

    center : array-like or None
        Coordinate pair around which to center the layout.

    store_pos_as : str, default None
        If non-None, the position of each node will be stored on the graph as
        an attribute with this string as its name, which can be accessed with
        ``G.nodes[...][store_pos_as]``. The function still returns the dictionary.

    Returns
    -------
    pos : dict
        A dictionary of positions keyed by node.

    Examples
    --------
    >>> from pprint import pprint
    >>> G = nx.path_graph(4)
    >>> pos = nx.bfs_layout(G, 0)
    >>> # suppress the returned dict and store on the graph directly
    >>> _ = nx.bfs_layout(G, 0, store_pos_as="pos")
    >>> pprint(nx.get_node_attributes(G, "pos"))
    {0: array([-1.,  0.]),
     1: array([-0.33333333,  0.        ]),
     2: array([0.33333333, 0.        ]),
     3: array([1., 0.])}



    Notes
    -----
    This algorithm currently only works in two dimensions and does not
    try to minimize edge crossings.

    """
    G, center = _process_params(G, center, 2)

    # Compute layers with BFS
    layers = dict(enumerate(nx.bfs_layers(G, start)))

    if len(G) != sum(len(nodes) for nodes in layers.values()):
        raise nx.NetworkXError(
            "bfs_layout didn't include all nodes. Perhaps use input graph:\n"
            "        G.subgraph(nx.node_connected_component(G, start))"
        )

    # Compute node positions with multipartite_layout
    pos = multipartite_layout(
        G, subset_key=layers, align=align, scale=scale, center=center
    )

    if store_pos_as is not None:
        nx.set_node_attributes(G, pos, store_pos_as)

    return pos

