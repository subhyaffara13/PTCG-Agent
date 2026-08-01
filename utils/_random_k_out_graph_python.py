
def _random_k_out_graph_python(n, k, alpha, self_loops=True, seed=None):
    G = nx.empty_graph(n, create_using=nx.MultiDiGraph)
    weights = Counter({v: alpha for v in G})
    out_strengths = Counter({v: 0 for v in G})

    for i in range(k * n):
        u = seed.choice(list(out_strengths.keys()))
        # If self-loops are not allowed, make the source node `u` have
        # weight zero.
        if not self_loops:
            uweight = weights.pop(u)

        v = weighted_choice(weights, seed=seed)

        if not self_loops:
            weights[u] = uweight

        G.add_edge(u, v)
        weights[v] += 1
        out_strengths[u] += 1
        if out_strengths[u] == k:
            out_strengths.pop(u)
    return G

