
def multipartite_layout(
    G, subset_key="subset", align="vertical", scale=1, center=None, store_pos_as=None
):
    """Position nodes in layers of straight lines.

    Parameters
    ----------
    G : NetworkX graph or list of nodes
        A position will be assigned to every node in G.

    subset_key : string or dict (default='subset')
        If a string, the key of node data in G that holds the node subset.
        If a dict, keyed by layer number to the nodes in that layer/subset.

    align : string (default='vertical')
        The alignment of nodes. Vertical or horizontal.

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
    >>> G = nx.complete_multipartite_graph(28, 16, 10)
    >>> pos = nx.multipartite_layout(G)
    >>> # suppress the returned dict and store on the graph directly
    >>> G = nx.complete_multipartite_graph(28, 16, 10)
    >>> _ = nx.multipartite_layout(G, store_pos_as="pos")

    or use a dict to provide the layers of the layout

    >>> G = nx.Graph([(0, 1), (1, 2), (1, 3), (3, 4)])
    >>> layers = {"a": [0], "b": [1], "c": [2, 3], "d": [4]}
    >>> pos = nx.multipartite_layout(G, subset_key=layers)

    Notes
    -----
    This algorithm currently only works in two dimensions and does not
    try to minimize edge crossings.

    Network does not need to be a complete multipartite graph. As long as nodes
    have subset_key data, they will be placed in the corresponding layers.

    """
    import numpy as np

    if align not in ("vertical", "horizontal"):
        msg = "align must be either vertical or horizontal."
        raise ValueError(msg)

    G, center = _process_params(G, center=center, dim=2)
    if len(G) == 0:
        return {}

    try:
        # check if subset_key is dict-like
        if len(G) != sum(len(nodes) for nodes in subset_key.values()):
            raise nx.NetworkXError(
                "all nodes must be in one subset of `subset_key` dict"
            )
    except AttributeError:
        # subset_key is not a dict, hence a string
        node_to_subset = nx.get_node_attributes(G, subset_key)
        if len(node_to_subset) != len(G):
            raise nx.NetworkXError(
                f"all nodes need a subset_key attribute: {subset_key}"
            )
        subset_key = nx.utils.groups(node_to_subset)

    # Sort by layer, if possible
    try:
        layers = dict(sorted(subset_key.items()))
    except TypeError:
        layers = subset_key

    pos = None
    nodes = []
    width = len(layers)
    for i, layer in enumerate(layers.values()):
        height = len(layer)
        xs = np.repeat(i, height)
        ys = np.arange(0, height, dtype=float)
        offset = ((width - 1) / 2, (height - 1) / 2)
        layer_pos = np.column_stack([xs, ys]) - offset
        if pos is None:
            pos = layer_pos
        else:
            pos = np.concatenate([pos, layer_pos])
        nodes.extend(layer)
    pos = rescale_layout(pos, scale=scale) + center
    if align == "horizontal":
        pos = pos[:, ::-1]  # swap x and y coords
    pos = dict(zip(nodes, pos))

    if store_pos_as is not None:
        nx.set_node_attributes(G, pos, store_pos_as)

    return pos

