
def spiral_layout(
    G,
    scale=1,
    center=None,
    dim=2,
    resolution=0.35,
    equidistant=False,
    store_pos_as=None,
):
    """Position nodes in a spiral layout.

    Parameters
    ----------
    G : NetworkX graph or list of nodes
        A position will be assigned to every node in G.

    scale : number (default: 1)
        Scale factor for positions.

    center : array-like or None
        Coordinate pair around which to center the layout.

    dim : int, default=2
        Dimension of layout, currently only dim=2 is supported.
        Other dimension values result in a ValueError.

    resolution : float, default=0.35
        The compactness of the spiral layout returned.
        Lower values result in more compressed spiral layouts.

    equidistant : bool, default=False
        If True, nodes will be positioned equidistant from each other
        by decreasing angle further from center.
        If False, nodes will be positioned at equal angles
        from each other by increasing separation further from center.

    store_pos_as : str, default None
        If non-None, the position of each node will be stored on the graph as
        an attribute with this string as its name, which can be accessed with
        ``G.nodes[...][store_pos_as]``. The function still returns the dictionary.

    Returns
    -------
    pos : dict
        A dictionary of positions keyed by node

    Raises
    ------
    ValueError
        If dim != 2

    Examples
    --------
    >>> from pprint import pprint
    >>> G = nx.path_graph(4)
    >>> pos = nx.spiral_layout(G)
    >>> nx.draw(G, pos=pos)
    >>> # suppress the returned dict and store on the graph directly
    >>> _ = nx.spiral_layout(G, store_pos_as="pos")
    >>> pprint(nx.get_node_attributes(G, "pos"))
    {0: array([-0.64153279, -0.68555087]),
     1: array([-0.03307913, -0.46344795]),
     2: array([0.34927952, 0.14899882]),
     3: array([0.32533239, 1.        ])}

    Notes
    -----
    This algorithm currently only works in two dimensions.

    """
    import numpy as np

    if dim != 2:
        raise ValueError("can only handle 2 dimensions")

    G, center = _process_params(G, center, dim)

    if len(G) == 0:
        return {}
    if len(G) == 1:
        pos = {nx.utils.arbitrary_element(G): center}
        if store_pos_as is not None:
            nx.set_node_attributes(G, pos, store_pos_as)
        return pos

    pos = []
    if equidistant:
        chord = 1
        step = 0.5
        theta = resolution
        theta += chord / (step * theta)
        for _ in range(len(G)):
            r = step * theta
            theta += chord / r
            pos.append([np.cos(theta) * r, np.sin(theta) * r])

    else:
        dist = np.arange(len(G), dtype=float)
        angle = resolution * dist
        pos = np.transpose(dist * np.array([np.cos(angle), np.sin(angle)]))

    pos = rescale_layout(np.array(pos), scale=scale) + center

    pos = dict(zip(G, pos))

    if store_pos_as is not None:
        nx.set_node_attributes(G, pos, store_pos_as)

    return pos

