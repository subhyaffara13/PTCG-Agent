
def _node_betweenness(G, source, cutoff=False, normalized=True, weight=None):
    """Node betweenness_centrality helper:

    See betweenness_centrality for what you probably want.
    This actually computes "load" and not betweenness.
    See https://networkx.lanl.gov/ticket/103

    This calculates the load of each node for paths from a single source.
    (The fraction of number of shortests paths from source that go
    through each node.)

    To get the load for a node you need to do all-pairs shortest paths.

    If weight is not None then use Dijkstra for finding shortest paths.
    """
    # get the predecessor and path length data
    if weight is None:
        (pred, length) = nx.predecessor(G, source, cutoff=cutoff, return_seen=True)
    else:
        (pred, length) = nx.dijkstra_predecessor_and_distance(G, source, cutoff, weight)

    # order the nodes by path length
    onodes = [(l, vert) for (vert, l) in length.items()]
    onodes.sort()
    onodes[:] = [vert for (l, vert) in onodes if l > 0]

    # initialize betweenness
    between = {}.fromkeys(length, 1.0)

    while onodes:
        v = onodes.pop()
        if v in pred:
            num_paths = len(pred[v])  # Discount betweenness if more than
            for x in pred[v]:  # one shortest path.
                if x == source:  # stop if hit source because all remaining v
                    break  # also have pred[v]==[source]
                between[x] += between[v] / num_paths
    #  remove source
    for v in between:
        between[v] -= 1
    # rescale to be between 0 and 1
    if normalized:
        l = len(between)
        if l > 2:
            # scale by 1/the number of possible paths
            scale = 1 / ((l - 1) * (l - 2))
            for v in between:
                between[v] *= scale
    return between

