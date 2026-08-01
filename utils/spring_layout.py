
def spring_layout(
    G,
    k=None,
    pos=None,
    fixed=None,
    iterations=50,
    threshold=1e-4,
    weight="weight",
    scale=1,
    center=None,
    dim=2,
    seed=None,
    store_pos_as=None,
    *,
    method="auto",
    gravity=1.0,
):
    """Position nodes using Fruchterman-Reingold force-directed algorithm.

    The algorithm simulates a force-directed representation of the network
    treating edges as springs holding nodes close, while treating nodes
    as repelling objects, sometimes called an anti-gravity force.
    Simulation continues until the positions are close to an equilibrium.

    There are some hard-coded values: minimal distance between
    nodes (0.01) and "temperature" of 0.1 to ensure nodes don't fly away.
    During the simulation, `k` helps determine the distance between nodes,
    though `scale` and `center` determine the size and place after
    rescaling occurs at the end of the simulation.

    Fixing some nodes doesn't allow them to move in the simulation.
    It also turns off the rescaling feature at the simulation's end.
    In addition, setting `scale` to `None` turns off rescaling.

    Parameters
    ----------
    G : NetworkX graph or list of nodes
        A position will be assigned to every node in G.

    k : float (default=None)
        Optimal distance between nodes.  If None the distance is set to
        1/sqrt(n) where n is the number of nodes.  Increase this value
        to move nodes farther apart.

    pos : dict or None  optional (default=None)
        Initial positions for nodes as a dictionary with node as keys
        and values as a coordinate list or tuple.  If None, then use
        random initial positions.

    fixed : list or None  optional (default=None)
        Nodes to keep fixed at initial position.
        Nodes not in ``G.nodes`` are ignored.
        ValueError raised if `fixed` specified and `pos` not.

    iterations : int  optional (default=50)
        Maximum number of iterations taken

    threshold: float optional (default = 1e-4)
        Threshold for relative error in node position changes.
        The iteration stops if the error is below this threshold.

    weight : string or None   optional (default='weight')
        The edge attribute that holds the numerical value used for
        the edge weight.  Larger means a stronger attractive force.
        If None, then all edge weights are 1.

    scale : number or None (default: 1)
        Scale factor for positions. Not used unless `fixed is None`.
        If scale is None, no rescaling is performed.

    center : array-like or None
        Coordinate pair around which to center the layout.
        Not used unless `fixed is None`.

    dim : int
        Dimension of layout.

    seed : int, RandomState instance or None  optional (default=None)
        Used only for the initial positions in the algorithm.
        Set the random state for deterministic node layouts.
        If int, `seed` is the seed used by the random number generator,
        if numpy.random.RandomState instance, `seed` is the random
        number generator,
        if None, the random number generator is the RandomState instance used
        by numpy.random.

    store_pos_as : str, default None
        If non-None, the position of each node will be stored on the graph as
        an attribute with this string as its name, which can be accessed with
        ``G.nodes[...][store_pos_as]``. The function still returns the dictionary.

    method : str  optional (default='auto')
        The method to compute the layout.
        If 'force', the force-directed Fruchterman-Reingold algorithm [1]_ is used.
        If 'energy', the energy-based optimization algorithm [2]_ is used with absolute
        values of edge weights and gravitational forces acting on each connected component.
        If 'auto', we use 'force' if ``len(G) < 500`` and 'energy' otherwise.

    gravity: float optional (default=1.0)
        Used only for the method='energy'.
        The positive coefficient of gravitational forces per connected component.

    Returns
    -------
    pos : dict
        A dictionary of positions keyed by node

    Examples
    --------
    >>> from pprint import pprint
    >>> G = nx.path_graph(4)
    >>> pos = nx.spring_layout(G)
    >>> # suppress the returned dict and store on the graph directly
    >>> _ = nx.spring_layout(G, seed=123, store_pos_as="pos")
    >>> pprint(nx.get_node_attributes(G, "pos"))
    {0: array([-0.61495802, -1.        ]),
     1: array([-0.21789544, -0.35432583]),
     2: array([0.21847843, 0.35527369]),
     3: array([0.61437502, 0.99905215])}


    # The same using longer but equivalent function name
    >>> pos = nx.fruchterman_reingold_layout(G)

    References
    ----------
    .. [1] Fruchterman, Thomas MJ, and Edward M. Reingold.
           "Graph drawing by force-directed placement."
           Software: Practice and experience 21, no. 11 (1991): 1129-1164.
           http://dx.doi.org/10.1002/spe.4380211102
    .. [2] Hamaguchi, Hiroki, Naoki Marumo, and Akiko Takeda.
           "Initial Placement for Fruchterman--Reingold Force Model With Coordinate Newton Direction."
           arXiv preprint arXiv:2412.20317 (2024).
           https://arxiv.org/abs/2412.20317
    """
    import numpy as np

    if method not in ("auto", "force", "energy"):
        raise ValueError("the method must be either auto, force, or energy.")
    if method == "auto":
        method = "force" if len(G) < 500 else "energy"

    G, center = _process_params(G, center, dim)

    if fixed is not None:
        if pos is None:
            raise ValueError("nodes are fixed without positions given")
        for node in fixed:
            if node not in pos:
                raise ValueError("nodes are fixed without positions given")
        nfixed = {node: i for i, node in enumerate(G)}
        fixed = np.asarray([nfixed[node] for node in fixed if node in nfixed])

    if pos is not None:
        # Determine size of existing domain to adjust initial positions
        dom_size = max(coord for pos_tup in pos.values() for coord in pos_tup)
        if dom_size == 0:
            dom_size = 1
        pos_arr = seed.rand(len(G), dim) * dom_size + center

        for i, n in enumerate(G):
            if n in pos:
                pos_arr[i] = np.asarray(pos[n])
    else:
        pos_arr = None
        dom_size = 1

    if len(G) == 0:
        return {}
    if len(G) == 1:
        pos = {nx.utils.arbitrary_element(G.nodes()): center}
        if store_pos_as is not None:
            nx.set_node_attributes(G, pos, store_pos_as)
        return pos

    # Sparse matrix
    if len(G) >= 500 or method == "energy":
        A = nx.to_scipy_sparse_array(G, weight=weight, dtype="f")
        if k is None and fixed is not None:
            # We must adjust k by domain size for layouts not near 1x1
            nnodes, _ = A.shape
            k = dom_size / np.sqrt(nnodes)
        pos = _sparse_fruchterman_reingold(
            A, k, pos_arr, fixed, iterations, threshold, dim, seed, method, gravity
        )
    else:
        A = nx.to_numpy_array(G, weight=weight)
        if k is None and fixed is not None:
            # We must adjust k by domain size for layouts not near 1x1
            nnodes, _ = A.shape
            k = dom_size / np.sqrt(nnodes)
        pos = _fruchterman_reingold(
            A, k, pos_arr, fixed, iterations, threshold, dim, seed
        )
    if fixed is None and scale is not None:
        pos = rescale_layout(pos, scale=scale) + center
    pos = dict(zip(G, pos))

    if store_pos_as is not None:
        nx.set_node_attributes(G, pos, store_pos_as)

    return pos

