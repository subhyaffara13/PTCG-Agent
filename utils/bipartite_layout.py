
def bipartite_layout(
    G,
    nodes=None,
    align="vertical",
    scale=1,
    center=None,
    aspect_ratio=4 / 3,
    store_pos_as=None,
):
    """Position nodes in two straight lines.

    Parameters
    ----------
    G : NetworkX graph or list of nodes
        A position will be assigned to every node in G.

    nodes : collection of nodes
        Nodes in one node set of the graph. This set will be placed on
        left or top. If `None` (the default), a node set is chosen arbitrarily
        if the graph if bipartite.

    align : string (default='vertical')
        The alignment of nodes. Vertical or horizontal.

    scale : number (default: 1)
        Scale factor for positions.

    center : array-like or None
        Coordinate pair around which to center the layout.

    aspect_ratio : number (default=4/3):
        The ratio of the width to the height of the layout.

    store_pos_as : str, default None
        If non-None, the position of each node will be stored on the graph as
        an attribute with this string as its name, which can be accessed with
        ``G.nodes[...][store_pos_as]``. The function still returns the dictionary.

    Returns
    -------
    pos : dict
        A dictionary of positions keyed by node.

    Raises
    ------
    NetworkXError
        If ``nodes=None`` and `G` is not bipartite.

    Examples
    --------
    >>> G = nx.complete_bipartite_graph(3, 3)
    >>> pos = nx.bipartite_layout(G)

    The ordering of the layout (i.e. which nodes appear on the left/top) can
    be specified with the `nodes` parameter:

    >>> top, bottom = nx.bipartite.sets(G)
    >>> pos = nx.bipartite_layout(G, nodes=bottom)  # "bottom" set appears on the left

    `store_pos_as` can be used to store the node positions for the computed layout
    directly on the nodes:

    >>> _ = nx.bipartite_layout(G, nodes=bottom, store_pos_as="pos")
    >>> from pprint import pprint
    >>> pprint(nx.get_node_attributes(G, "pos"))
    {0: array([ 1.  , -0.75]),
     1: array([1., 0.]),
     2: array([1.  , 0.75]),
     3: array([-1.  , -0.75]),
     4: array([-1.,  0.]),
     5: array([-1.  ,  0.75])}


    The ``bipartite_layout`` function can be used with non-bipartite graphs
    by explicitly specifying how the layout should be partitioned with `nodes`:

    >>> G = nx.complete_graph(5)  # Non-bipartite
    >>> pos = nx.bipartite_layout(G, nodes={0, 1, 2})

    Notes
    -----
    This algorithm currently only works in two dimensions and does not
    try to minimize edge crossings.

    """

    import numpy as np

    if align not in ("vertical", "horizontal"):
        msg = "align must be either vertical or horizontal."
        raise ValueError(msg)

    G, center = _process_params(G, center=center, dim=2)
    if len(G) == 0:
        return {}

    height = 1
    width = aspect_ratio * height
    offset = (width / 2, height / 2)

    if nodes is None:
        top, bottom = nx.bipartite.sets(G)
        nodes = list(G)
    else:
        top = set(nodes)
        bottom = set(G) - top
        # Preserves backward-compatible node ordering in returned pos dict
        nodes = list(top) + list(bottom)

    left_xs = np.repeat(0, len(top))
    right_xs = np.repeat(width, len(bottom))
    left_ys = np.linspace(0, height, len(top))
    right_ys = np.linspace(0, height, len(bottom))

    top_pos = np.column_stack([left_xs, left_ys]) - offset
    bottom_pos = np.column_stack([right_xs, right_ys]) - offset

    pos = np.concatenate([top_pos, bottom_pos])
    pos = rescale_layout(pos, scale=scale) + center
    if align == "horizontal":
        pos = pos[:, ::-1]  # swap x and y coords
    pos = dict(zip(nodes, pos))

    if store_pos_as is not None:
        nx.set_node_attributes(G, pos, store_pos_as)

    return pos

