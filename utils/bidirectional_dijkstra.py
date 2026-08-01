
def bidirectional_dijkstra(G, source, target, weight="weight"):
    r"""Dijkstra's algorithm for shortest paths using bidirectional search.

    Parameters
    ----------
    G : NetworkX graph

    source : node
        Starting node.

    target : node
        Ending node.

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

    Returns
    -------
    length, path : number and list
        length is the distance from source to target.
        path is a list of nodes on a path from source to target.

    Raises
    ------
    NodeNotFound
        If `source` or `target` is not in `G`.

    NetworkXNoPath
        If no path exists between source and target.

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> length, path = nx.bidirectional_dijkstra(G, 0, 4)
    >>> print(length)
    4
    >>> print(path)
    [0, 1, 2, 3, 4]

    Notes
    -----
    Edge weight attributes must be numerical.
    Distances are calculated as sums of weighted edges traversed.

    The weight function can be used to hide edges by returning None.
    So ``weight = lambda u, v, d: 1 if d['color']=="red" else None``
    will find the shortest red path.

    In practice  bidirectional Dijkstra is much more than twice as fast as
    ordinary Dijkstra.

    Ordinary Dijkstra expands nodes in a sphere-like manner from the
    source. The radius of this sphere will eventually be the length
    of the shortest path. Bidirectional Dijkstra will expand nodes
    from both the source and the target, making two spheres of half
    this radius. Volume of the first sphere is `\pi*r*r` while the
    others are `2*\pi*r/2*r/2`, making up half the volume.

    This algorithm is not guaranteed to work if edge weights
    are negative or are floating point numbers
    (overflows and roundoff errors can cause problems).

    See Also
    --------
    shortest_path
    shortest_path_length
    """
    if source not in G:
        raise nx.NodeNotFound(f"Source {source} is not in G")

    if target not in G:
        raise nx.NodeNotFound(f"Target {target} is not in G")

    if source == target:
        return (0, [source])

    weight = _weight_function(G, weight)
    # Init:  [Forward, Backward]
    dists = [{}, {}]  # dictionary of final distances
    preds = [{source: None}, {target: None}]  # dictionary of preds

    def path(curr, direction):
        ret = []
        while curr is not None:
            ret.append(curr)
            curr = preds[direction][curr]
        return list(reversed(ret)) if direction == 0 else ret

    fringe = [[], []]  # heap of (distance, node) for choosing node to expand
    seen = [{source: 0}, {target: 0}]  # dict of distances to seen nodes
    c = count()
    # initialize fringe heap
    heappush(fringe[0], (0, next(c), source))
    heappush(fringe[1], (0, next(c), target))
    # neighbors for extracting correct neighbor information
    if G.is_directed():
        neighbors = [G._succ, G._pred]
    else:
        neighbors = [G._adj, G._adj]
    # variables to hold shortest discovered path
    finaldist = None
    meetnode = None
    direction = 1
    while fringe[0] and fringe[1]:
        # choose direction
        # direction == 0 is forward direction and direction == 1 is back
        direction = 1 - direction
        # extract closest to expand
        (dist, _, v) = heappop(fringe[direction])
        if v in dists[direction]:
            # Shortest path to v has already been found
            continue
        # update distance
        dists[direction][v] = dist  # equal to seen[direction][v]
        if v in dists[1 - direction]:
            # if we have scanned v in both directions we are done
            # we have now discovered the shortest path
            return (finaldist, path(meetnode, 0) + path(preds[1][meetnode], 1))

        for w, d in neighbors[direction][v].items():
            # weight(v, w, d) for forward and weight(w, v, d) for back direction
            cost = weight(v, w, d) if direction == 0 else weight(w, v, d)
            if cost is None:
                continue
            vwLength = dist + cost
            if w in dists[direction]:
                if vwLength < dists[direction][w]:
                    raise ValueError("Contradictory paths found: negative weights?")
            elif w not in seen[direction] or vwLength < seen[direction][w]:
                # relaxing
                seen[direction][w] = vwLength
                heappush(fringe[direction], (vwLength, next(c), w))
                preds[direction][w] = v
                if w in seen[1 - direction]:
                    # see if this path is better than the already
                    # discovered shortest path
                    finaldist_w = vwLength + seen[1 - direction][w]
                    if finaldist is None or finaldist > finaldist_w:
                        finaldist, meetnode = finaldist_w, w
    raise nx.NetworkXNoPath(f"No path between {source} and {target}.")

