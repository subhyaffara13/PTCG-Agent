
def triangles(G, nodes=None):
    """Compute the number of triangles.

    Finds the number of triangles that include a node as one vertex.

    Parameters
    ----------
    G : graph
       A networkx graph

    nodes : node, iterable of nodes, or None (default=None)
        If a singleton node, return the number of triangles for that node.
        If an iterable, compute the number of triangles for each of those nodes.
        If `None` (the default) compute the number of triangles for all nodes in `G`.

    Returns
    -------
    out : dict or int
       If `nodes` is a container of nodes, returns number of triangles keyed by node (dict).
       If `nodes` is a specific node, returns number of triangles for the node (int).

    Examples
    --------
    >>> G = nx.complete_graph(5)
    >>> print(nx.triangles(G, 0))
    6
    >>> print(nx.triangles(G))
    {0: 6, 1: 6, 2: 6, 3: 6, 4: 6}
    >>> print(list(nx.triangles(G, [0, 1]).values()))
    [6, 6]

    The total number of unique triangles in `G` can be determined by summing
    the number of triangles for each node and dividing by 3 (because a given
    triangle gets counted three times, once for each of its nodes).

    >>> sum(nx.triangles(G).values()) // 3
    10

    Notes
    -----
    Self loops are ignored.

    """
    if nodes is not None:
        # If `nodes` represents a single node, return only its number of triangles
        if nodes in G:
            return next(_triangles_and_degree_iter(G, nodes))[2] // 2

        # if `nodes` is a container of nodes, then return a
        # dictionary mapping node to number of triangles.
        return {v: t // 2 for v, d, t, _ in _triangles_and_degree_iter(G, nodes)}

    # if nodes is None, then compute triangles for the complete graph

    # dict used to avoid visiting the same nodes twice
    # this allows calculating/counting each triangle only once
    later_nbrs = {}

    # iterate over the nodes in a graph
    for node, neighbors in G.adjacency():
        later_nbrs[node] = {n for n in neighbors if n not in later_nbrs and n != node}

    # instantiate Counter for each node to include isolated nodes
    # add 1 to the count if a nodes neighbor's neighbor is also a neighbor
    triangle_counts = Counter(dict.fromkeys(G, 0))
    for node1, neighbors in later_nbrs.items():
        for node2 in neighbors:
            third_nodes = neighbors & later_nbrs[node2]
            m = len(third_nodes)
            triangle_counts[node1] += m
            triangle_counts[node2] += m
            triangle_counts.update(third_nodes)

    return dict(triangle_counts)


def triangles(creation_sequence):
    """
    Compute number of triangles in the threshold graph with the
    given creation sequence.
    """
    # shortcut algorithm that doesn't require computing number
    # of triangles at each node.
    cs = creation_sequence  # alias
    dr = cs.count("d")  # number of d's in sequence
    ntri = dr * (dr - 1) * (dr - 2) / 6  # number of triangles in clique of nd d's
    # now add dr choose 2 triangles for every 'i' in sequence where
    # dr is the number of d's to the right of the current i
    for i, typ in enumerate(cs):
        if typ == "i":
            ntri += dr * (dr - 1) / 2
        else:
            dr -= 1
    return ntri

