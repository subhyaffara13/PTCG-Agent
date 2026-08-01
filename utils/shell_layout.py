
def shell_layout(
    G, nlist=None, rotate=None, scale=1, center=None, dim=2, store_pos_as=None
):
    """Position nodes in concentric circles.

    Parameters
    ----------
    G : NetworkX graph or list of nodes
        A position will be assigned to every node in G.

    nlist : list of lists
       List of node lists for each shell.

    rotate : angle in radians (default=pi/len(nlist))
       Angle by which to rotate the starting position of each shell
       relative to the starting position of the previous shell.
       To recreate behavior before v2.5 use rotate=0.

    scale : number (default: 1)
        Scale factor for positions.

    center : array-like or None
        Coordinate pair around which to center the layout.

    dim : int
        Dimension of layout, currently only dim=2 is supported.
        Other dimension values result in a ValueError.

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
    >>> shells = [[0], [1, 2, 3]]
    >>> pos = nx.shell_layout(G, shells)
    >>> # suppress the returned dict and store on the graph directly
    >>> _ = nx.shell_layout(G, shells, store_pos_as="pos")
    >>> pprint(nx.get_node_attributes(G, "pos"))
    {0: array([0., 0.]),
     1: array([-5.00000000e-01, -4.37113883e-08]),
     2: array([ 0.24999996, -0.43301272]),
     3: array([0.24999981, 0.43301281])}

    Notes
    -----
    This algorithm currently only works in two dimensions and does not
    try to minimize edge crossings.

    """
    import numpy as np

    if dim != 2:
        raise ValueError("can only handle 2 dimensions")

    G, center = _process_params(G, center, dim)

    if len(G) == 0:
        return {}
    if len(G) == 1:
        return {nx.utils.arbitrary_element(G): center}

    if nlist is None:
        # draw the whole graph in one shell
        nlist = [list(G)]

    radius_bump = scale / len(nlist)

    if len(nlist[0]) == 1:
        # single node at center
        radius = 0.0
    else:
        # else start at r=1
        radius = radius_bump

    if rotate is None:
        rotate = np.pi / len(nlist)
    first_theta = rotate
    npos = {}
    for nodes in nlist:
        # Discard the last angle (endpoint=False) since 2*pi matches 0 radians
        theta = (
            np.linspace(0, 2 * np.pi, len(nodes), endpoint=False, dtype=np.float32)
            + first_theta
        )
        pos = radius * np.column_stack([np.cos(theta), np.sin(theta)]) + center
        npos.update(zip(nodes, pos))
        radius += radius_bump
        first_theta += rotate

    if store_pos_as is not None:
        nx.set_node_attributes(G, npos, store_pos_as)
    return npos

