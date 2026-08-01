
def kamada_kawai_layout(
    G,
    dist=None,
    pos=None,
    weight="weight",
    scale=1,
    center=None,
    dim=2,
    store_pos_as=None,
):
    """Position nodes using Kamada-Kawai path-length cost-function.

    Parameters
    ----------
    G : NetworkX graph or list of nodes
        A position will be assigned to every node in G.

    dist : dict (default=None)
        A two-level dictionary of optimal distances between nodes,
        indexed by source and destination node.
        If None, the distance is computed using shortest_path_length().

    pos : dict or None  optional (default=None)
        Initial positions for nodes as a dictionary with node as keys
        and values as a coordinate list or tuple.  If None, then use
        circular_layout() for dim >= 2 and a linear layout for dim == 1.

    weight : string or None   optional (default='weight')
        The edge attribute that holds the numerical value used for
        the edge weight.  If None, then all edge weights are 1.

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

    Examples
    --------
    >>> from pprint import pprint
    >>> G = nx.path_graph(4)
    >>> pos = nx.kamada_kawai_layout(G)
    >>> # suppress the returned dict and store on the graph directly
    >>> _ = nx.kamada_kawai_layout(G, store_pos_as="pos")
    >>> pprint(nx.get_node_attributes(G, "pos"))
    {0: array([0.99996577, 0.99366857]),
     1: array([0.32913544, 0.33543827]),
     2: array([-0.33544334, -0.32910684]),
     3: array([-0.99365787, -1.        ])}
    """
    import numpy as np

    G, center = _process_params(G, center, dim)
    nNodes = len(G)
    if nNodes == 0:
        return {}

    if dist is None:
        dist = dict(nx.shortest_path_length(G, weight=weight))
    dist_mtx = 1e6 * np.ones((nNodes, nNodes))
    for row, nr in enumerate(G):
        if nr not in dist:
            continue
        rdist = dist[nr]
        for col, nc in enumerate(G):
            if nc not in rdist:
                continue
            dist_mtx[row][col] = rdist[nc]

    if pos is None:
        if dim >= 3:
            pos = random_layout(G, dim=dim)
        elif dim == 2:
            pos = circular_layout(G, dim=dim)
        else:
            pos = dict(zip(G, np.linspace(0, 1, len(G))))
    pos_arr = np.array([pos[n] for n in G])

    pos = _kamada_kawai_solve(dist_mtx, pos_arr, dim)

    pos = rescale_layout(pos, scale=scale) + center
    pos = dict(zip(G, pos))

    if store_pos_as is not None:
        nx.set_node_attributes(G, pos, store_pos_as)

    return pos

