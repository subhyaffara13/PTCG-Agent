
def astar_path_length(
    G, source, target, heuristic=None, weight="weight", *, cutoff=None
):
    """Returns the length of the shortest path between source and target using
    the A* ("A-star") algorithm.

    Parameters
    ----------
    G : NetworkX graph

    source : node
       Starting node for path

    target : node
       Ending node for path

    heuristic : function
       A function to evaluate the estimate of the distance
       from the a node to the target.  The function takes
       two nodes arguments and must return a number.
       If the heuristic is inadmissible (if it might
       overestimate the cost of reaching the goal from a node),
       the result may not be a shortest path.
       The algorithm does not support updating heuristic
       values for the same node due to caching the first
       heuristic calculation per node.

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
       return a number or None to indicate a hidden edge.

    cutoff : float, optional
       If this is provided, the search will be bounded to this value. I.e. if
       the evaluation function surpasses this value for a node n, the node will not
       be expanded further and will be ignored. More formally, let h'(n) be the
       heuristic function, and g(n) be the cost of reaching n from the source node. Then,
       if g(n) + h'(n) > cutoff, the node will not be explored further.
       Note that if the heuristic is inadmissible, it is possible that paths
       are ignored even though they satisfy the cutoff.

    Raises
    ------
    NetworkXNoPath
        If no path exists between source and target.

    See Also
    --------
    astar_path

    """
    if source not in G or target not in G:
        msg = f"Either source {source} or target {target} is not in G"
        raise nx.NodeNotFound(msg)

    weight = _weight_function(G, weight)
    path = astar_path(G, source, target, heuristic, weight, cutoff=cutoff)
    return sum(weight(u, v, G[u][v]) for u, v in zip(path[:-1], path[1:]))

