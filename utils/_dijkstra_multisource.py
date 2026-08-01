
def _dijkstra_multisource(
    G, sources, weight, pred=None, paths=None, cutoff=None, target=None
):
    """Uses Dijkstra's algorithm to find shortest weighted paths

    Parameters
    ----------
    G : NetworkX graph

    sources : non-empty iterable of nodes
        Starting nodes for paths. If this is just an iterable containing
        a single node, then all paths computed by this function will
        start from that node. If there are two or more nodes in this
        iterable, the computed paths may begin from any one of the start
        nodes.

    weight: function
        Function with (u, v, data) input that returns that edge's weight
        or None to indicate a hidden edge

    pred: dict of lists, optional(default=None)
        dict to store a list of predecessors keyed by that node
        If None, predecessors are not stored.

    paths: dict, optional (default=None)
        dict to store the path list from source to each node, keyed by node.
        If None, paths are not stored.

    target : node label, optional
        Ending node for path. Search is halted when target is found.

    cutoff : integer or float, optional
        Length (sum of edge weights) at which the search is stopped.
        If cutoff is provided, only return paths with summed weight <= cutoff.

    Returns
    -------
    distance : dictionary
        A mapping from node to shortest distance to that node from one
        of the source nodes.

    Raises
    ------
    NodeNotFound
        If any of `sources` is not in `G`.

    Notes
    -----
    The optional predecessor and path dictionaries can be accessed by
    the caller through the original pred and paths objects passed
    as arguments. No need to explicitly return pred or paths.

    """
    # If `paths` is specified, we use a temporary internal dictionary (`pred_dict`) to
    # store predecessors, used to reconstruct paths. However, if the caller
    # passed in a `pred` dictionary, we must compute *all* predecessors, since the caller
    # expects the full predecessor structure.
    pred_dict = pred if paths is None or pred is not None else {}

    G_succ = G._adj  # For speed-up (and works for both directed and undirected graphs)

    dist = {}  # dictionary of final distances
    seen = {}
    # fringe is heapq with 3-tuples (distance,c,node)
    # use the count c to avoid comparing nodes (may not be able to)
    c = count()
    fringe = []
    for source in sources:
        seen[source] = 0
        heappush(fringe, (0, next(c), source))
    number_of_sources = len(seen)
    while fringe:
        (dist_v, _, v) = heappop(fringe)
        if v in dist:
            continue  # already searched this node.
        dist[v] = dist_v
        if v == target:
            break
        for u, e in G_succ[v].items():
            cost = weight(v, u, e)
            if cost is None:
                continue
            vu_dist = dist_v + cost
            if cutoff is not None and vu_dist > cutoff:
                continue
            if u in dist:
                u_dist = dist[u]
                if vu_dist < u_dist:
                    raise ValueError("Contradictory paths found:", "negative weights?")
                elif pred is not None and vu_dist == u_dist:
                    # Found another shortest path to u with equal distance (including zero-weight edges).
                    # We must store *all* predecessors because `pred` was provided by the caller.
                    pred_dict[u].append(v)
            elif u not in seen or vu_dist < seen[u]:
                seen[u] = vu_dist
                heappush(fringe, (vu_dist, next(c), u))
                if pred_dict is not None:
                    pred_dict[u] = [v]
            elif pred is not None and vu_dist == seen[u]:
                # Found another shortest path to u
                # We must store *all* predecessors because `pred` was provided by the caller.
                pred_dict[u].append(v)

    if paths is not None:
        # Reconstruct the path from source to target using the predecessor dictionary.
        if target is None:
            # Since `dist` is in increasing distance order, each predecessor's path is
            # already computed by the time we process `v`. We skip the first
            # `number_of_sources` entries because sources already have their paths defined.
            for v in islice(dist, number_of_sources, None):
                # `v` must be in `pred_dict`: any node with a distance (and not a source)
                # has a predecessor.
                paths[v] = paths[pred_dict[v][0]] + [v]
        else:
            # Caller requested the path to a specific target node.
            path = paths[target] = [target]
            while (current_preds := pred_dict.get(path[-1])) is not None:
                path.append(current_preds[0])
            # The path was built in reverse order, so reverse it at the end.
            path.reverse()

    # The optional predecessor and path dictionaries can be accessed
    # by the caller via the pred and paths objects passed as arguments.
    return dist

