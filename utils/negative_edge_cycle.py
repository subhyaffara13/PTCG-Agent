
def negative_edge_cycle(G, weight="weight", heuristic=True):
    """Returns True if there exists a negative edge cycle anywhere in G.

    Parameters
    ----------
    G : NetworkX graph

    weight : string or function
        If this is a string, then edge weights will be accessed via the
        edge attribute with this key (that is, the weight of the edge
        joining `u` to `v` will be ``G.edges[u, v][weight]``). If no
        such edge attribute exists, the weight of the edge is assumed to
        be one.

        If this is a function, the weight of an edge is the value
        returned by the function. The function must accept exactly three
        positional arguments: the two endpoints of an edge and the
        dictionary of edge attributes for that edge. The function must
        return a number.

    heuristic : bool
        Determines whether to use a heuristic to early detect negative
        cycles at a negligible cost. In case of graphs with a negative cycle,
        the performance of detection increases by at least an order of magnitude.

    Returns
    -------
    negative_cycle : bool
        True if a negative edge cycle exists, otherwise False.

    Examples
    --------
    >>> G = nx.cycle_graph(5, create_using=nx.DiGraph())
    >>> print(nx.negative_edge_cycle(G))
    False
    >>> G[1][2]["weight"] = -7
    >>> print(nx.negative_edge_cycle(G))
    True

    Notes
    -----
    Edge weight attributes must be numerical.
    Distances are calculated as sums of weighted edges traversed.

    This algorithm uses bellman_ford_predecessor_and_distance() but finds
    negative cycles on any component by first adding a new node connected to
    every node, and starting bellman_ford_predecessor_and_distance on that
    node.  It then removes that extra node.
    """
    if G.size() == 0:
        return False

    # find unused node to use temporarily
    newnode = -1
    while newnode in G:
        newnode -= 1
    # connect it to all nodes
    G.add_edges_from([(newnode, n) for n in G])

    try:
        bellman_ford_predecessor_and_distance(
            G, newnode, weight=weight, heuristic=heuristic
        )
    except nx.NetworkXUnbounded:
        return True
    finally:
        G.remove_node(newnode)
    return False

