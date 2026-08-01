
def dinitz_impl(G, s, t, capacity, residual, cutoff):
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

    # Initialize/reset the residual network.
    for u in R:
        for e in R[u].values():
            e["flow"] = 0

    # Use an arbitrary high value as infinite. It is computed
    # when building the residual network.
    INF = R.graph["inf"]

    if cutoff is None:
        cutoff = INF

    R_succ = R.succ
    R_pred = R.pred

    def breath_first_search():
        parents = {}
        vertex_dist = {s: 0}
        queue = deque([(s, 0)])
        # Record all the potential edges of shortest augmenting paths
        while queue:
            if t in parents:
                break
            u, dist = queue.popleft()
            for v, attr in R_succ[u].items():
                if attr["capacity"] - attr["flow"] > 0:
                    if v in parents:
                        if vertex_dist[v] == dist + 1:
                            parents[v].append(u)
                    else:
                        parents[v] = deque([u])
                        vertex_dist[v] = dist + 1
                        queue.append((v, dist + 1))
        return parents

    def depth_first_search(parents):
        # DFS to find all the shortest augmenting paths
        """Build a path using DFS starting from the sink"""
        total_flow = 0
        u = t
        # path also functions as a stack
        path = [u]
        # The loop ends with no augmenting path left in the layered graph
        while True:
            if len(parents[u]) > 0:
                v = parents[u][0]
                path.append(v)
            else:
                path.pop()
                if len(path) == 0:
                    break
                v = path[-1]
                parents[v].popleft()
            # Augment the flow along the path found
            if v == s:
                flow = INF
                for u, v in pairwise(path):
                    flow = min(flow, R_pred[u][v]["capacity"] - R_pred[u][v]["flow"])
                for u, v in pairwise(reversed(path)):
                    R_pred[v][u]["flow"] += flow
                    R_pred[u][v]["flow"] -= flow
                    # Find the proper node to continue the search
                    if R_pred[v][u]["capacity"] - R_pred[v][u]["flow"] == 0:
                        parents[v].popleft()
                        while path[-1] != v:
                            path.pop()
                total_flow += flow
                v = path[-1]
            u = v
        return total_flow

    flow_value = 0
    while flow_value < cutoff:
        parents = breath_first_search()
        if t not in parents:
            break
        this_flow = depth_first_search(parents)
        if this_flow * 2 > INF:
            raise nx.NetworkXUnbounded("Infinite capacity path, flow unbounded above.")
        flow_value += this_flow

    R.graph["flow_value"] = flow_value
    return R

