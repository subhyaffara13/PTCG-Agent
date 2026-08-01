
def shortest_augmenting_path_impl(G, s, t, capacity, residual, two_phase, cutoff):
    """Implementation of the shortest augmenting path algorithm."""
    if s not in G:
        raise nx.NetworkXError(f"node {str(s)} not in graph")
    if t not in G:
        raise nx.NetworkXError(f"node {str(t)} not in graph")
    if s == t:
        raise nx.NetworkXError("source and sink are the same node")

    if residual is None:
        R = build_residual_network(G, capacity)
    else:
        R = residual

    R_nodes = R.nodes
    R_pred = R.pred
    R_succ = R.succ

    # Initialize/reset the residual network.
    for u in R:
        for e in R_succ[u].values():
            e["flow"] = 0

    # Initialize heights of the nodes.
    heights = {t: 0}
    q = deque([(t, 0)])
    while q:
        u, height = q.popleft()
        height += 1
        for v, attr in R_pred[u].items():
            if v not in heights and attr["flow"] < attr["capacity"]:
                heights[v] = height
                q.append((v, height))

    if s not in heights:
        # t is not reachable from s in the residual network. The maximum flow
        # must be zero.
        R.graph["flow_value"] = 0
        return R

    n = len(G)
    m = R.size() / 2

    # Initialize heights and 'current edge' data structures of the nodes.
    for u in R:
        R_nodes[u]["height"] = heights[u] if u in heights else n
        R_nodes[u]["curr_edge"] = CurrentEdge(R_succ[u])

    # Initialize counts of nodes in each level.
    counts = [0] * (2 * n - 1)
    for u in R:
        counts[R_nodes[u]["height"]] += 1

    inf = R.graph["inf"]

    def augment(path):
        """Augment flow along a path from s to t."""
        # Determine the path residual capacity.
        flow = inf
        it = iter(path)
        u = next(it)
        for v in it:
            attr = R_succ[u][v]
            flow = min(flow, attr["capacity"] - attr["flow"])
            u = v
        if flow * 2 > inf:
            raise nx.NetworkXUnbounded("Infinite capacity path, flow unbounded above.")
        # Augment flow along the path.
        it = iter(path)
        u = next(it)
        for v in it:
            R_succ[u][v]["flow"] += flow
            R_succ[v][u]["flow"] -= flow
            u = v
        return flow

    def relabel(u):
        """Relabel a node to create an admissible edge."""
        height = n - 1
        for v, attr in R_succ[u].items():
            if attr["flow"] < attr["capacity"]:
                height = min(height, R_nodes[v]["height"])
        return height + 1

    if cutoff is None:
        cutoff = float("inf")

    # Phase 1: Look for shortest augmenting paths using depth-first search.

    flow_value = 0
    path = [s]
    u = s
    d = n if not two_phase else int(min(m**0.5, 2 * n ** (2.0 / 3)))
    done = R_nodes[s]["height"] >= d
    while not done:
        height = R_nodes[u]["height"]
        curr_edge = R_nodes[u]["curr_edge"]
        # Depth-first search for the next node on the path to t.
        while True:
            v, attr = curr_edge.get()
            if height == R_nodes[v]["height"] + 1 and attr["flow"] < attr["capacity"]:
                # Advance to the next node following an admissible edge.
                path.append(v)
                u = v
                break
            try:
                curr_edge.move_to_next()
            except StopIteration:
                counts[height] -= 1
                if counts[height] == 0:
                    # Gap heuristic: If relabeling causes a level to become
                    # empty, a minimum cut has been identified. The algorithm
                    # can now be terminated.
                    R.graph["flow_value"] = flow_value
                    return R
                height = relabel(u)
                if u == s and height >= d:
                    if not two_phase:
                        # t is disconnected from s in the residual network. No
                        # more augmenting paths exist.
                        R.graph["flow_value"] = flow_value
                        return R
                    else:
                        # t is at least d steps away from s. End of phase 1.
                        done = True
                        break
                counts[height] += 1
                R_nodes[u]["height"] = height
                if u != s:
                    # After relabeling, the last edge on the path is no longer
                    # admissible. Retreat one step to look for an alternative.
                    path.pop()
                    u = path[-1]
                    break
        if u == t:
            # t is reached. Augment flow along the path and reset it for a new
            # depth-first search.
            flow_value += augment(path)
            if flow_value >= cutoff:
                R.graph["flow_value"] = flow_value
                return R
            path = [s]
            u = s

    # Phase 2: Look for shortest augmenting paths using breadth-first search.
    flow_value += edmonds_karp_core(R, s, t, cutoff - flow_value)

    R.graph["flow_value"] = flow_value
    return R

