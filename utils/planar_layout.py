
def planar_layout(G, scale=1, center=None, dim=2, store_pos_as=None):
    """Position nodes without edge intersections.

    Parameters
    ----------
    G : NetworkX graph or list of nodes
        A position will be assigned to every node in G. If G is of type
        nx.PlanarEmbedding, the positions are selected accordingly.

    scale : number (default: 1)
        Scale factor for positions.

    center : array-like or None
        Coordinate pair around which to center the layout.

    dim : int
        Dimension of layout.

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
    NetworkXException
        If G is not planar

    Examples
    --------
    >>> from pprint import pprint
    >>> G = nx.path_graph(4)
    >>> pos = nx.planar_layout(G)
    >>> # suppress the returned dict and store on the graph directly
    >>> _ = nx.planar_layout(G, store_pos_as="pos")
    >>> pprint(nx.get_node_attributes(G, "pos"))
    {0: array([-0.77777778, -0.33333333]),
     1: array([ 1.        , -0.33333333]),
     2: array([0.11111111, 0.55555556]),
     3: array([-0.33333333,  0.11111111])}
    """
    import numpy as np

    if dim != 2:
        raise ValueError("can only handle 2 dimensions")

    G, center = _process_params(G, center, dim)

    if len(G) == 0:
        return {}

    if isinstance(G, nx.PlanarEmbedding):
        embedding = G
    else:
        is_planar, embedding = nx.check_planarity(G)
        if not is_planar:
            raise nx.NetworkXException("G is not planar.")
    pos = nx.combinatorial_embedding_to_pos(embedding)
    node_list = list(embedding)
    pos = np.vstack([pos[x] for x in node_list])
    pos = pos.astype(np.float64)
    pos = rescale_layout(pos, scale=scale) + center
    pos = dict(zip(node_list, pos))
    if store_pos_as is not None:
        nx.set_node_attributes(G, pos, store_pos_as)
    return pos

