
def onion_layers(G):
    """Returns the layer of each vertex in an onion decomposition of the graph.

    The onion decomposition refines the k-core decomposition by providing
    information on the internal organization of each k-shell. It is usually
    used alongside the `core numbers`.

    Parameters
    ----------
    G : NetworkX graph
        An undirected graph without self loops.

    Returns
    -------
    od_layers : dictionary
        A dictionary keyed by node to the onion layer. The layers are
        contiguous integers starting at 1.

    Raises
    ------
    NetworkXNotImplemented
        If `G` is a multigraph or directed graph or if it contains self loops.

    Examples
    --------
    >>> degrees = [0, 1, 2, 2, 2, 2, 3]
    >>> H = nx.havel_hakimi_graph(degrees)
    >>> H.degree
    DegreeView({0: 1, 1: 2, 2: 2, 3: 2, 4: 2, 5: 3, 6: 0})
    >>> nx.onion_layers(H)
    {6: 1, 0: 2, 4: 3, 1: 4, 2: 4, 3: 4, 5: 4}

    See Also
    --------
    core_number

    References
    ----------
    .. [1] Multi-scale structure and topological anomaly detection via a new
       network statistic: The onion decomposition
       L. Hébert-Dufresne, J. A. Grochow, and A. Allard
       Scientific Reports 6, 31708 (2016)
       http://doi.org/10.1038/srep31708
    .. [2] Percolation and the effective structure of complex networks
       A. Allard and L. Hébert-Dufresne
       Physical Review X 9, 011023 (2019)
       http://doi.org/10.1103/PhysRevX.9.011023
    """
    if nx.number_of_selfloops(G) > 0:
        msg = (
            "Input graph contains self loops which is not permitted; "
            "Consider using G.remove_edges_from(nx.selfloop_edges(G))."
        )
        raise nx.NetworkXNotImplemented(msg)
    # Dictionaries to register the k-core/onion decompositions.
    od_layers = {}
    # Adjacency list
    neighbors = {v: list(nx.all_neighbors(G, v)) for v in G}
    # Effective degree of nodes.
    degrees = dict(G.degree())
    # Performs the onion decomposition.
    current_core = 1
    current_layer = 1
    # Sets vertices of degree 0 to layer 1, if any.
    isolated_nodes = list(nx.isolates(G))
    if len(isolated_nodes) > 0:
        for v in isolated_nodes:
            od_layers[v] = current_layer
            degrees.pop(v)
        current_layer = 2
    # Finds the layer for the remaining nodes.
    while len(degrees) > 0:
        # Sets the order for looking at nodes.
        nodes = sorted(degrees, key=degrees.get)
        # Sets properly the current core.
        min_degree = degrees[nodes[0]]
        if min_degree > current_core:
            current_core = min_degree
        # Identifies vertices in the current layer.
        this_layer = []
        for n in nodes:
            if degrees[n] > current_core:
                break
            this_layer.append(n)
        # Identifies the core/layer of the vertices in the current layer.
        for v in this_layer:
            od_layers[v] = current_layer
            for n in neighbors[v]:
                neighbors[n].remove(v)
                degrees[n] = degrees[n] - 1
            degrees.pop(v)
        # Updates the layer count.
        current_layer = current_layer + 1
    # Returns the dictionaries containing the onion layer of each vertices.
    return od_layers

