
def _random_k_out_graph_numpy(n, k, alpha, self_loops=True, seed=None):
    import numpy as np

    G = nx.empty_graph(n, create_using=nx.MultiDiGraph)
    nodes = np.arange(n)
    remaining_mask = np.full(n, True)
    weights = np.full(n, alpha)
    total_weight = n * alpha
    out_strengths = np.zeros(n)

    for i in range(k * n):
        u = seed.choice(nodes[remaining_mask])

        if self_loops:
            v = seed.choice(nodes, p=weights / total_weight)
        else:  # Ignore weight of u when selecting v
            u_weight = weights[u]
            weights[u] = 0
            v = seed.choice(nodes, p=weights / (total_weight - u_weight))
            weights[u] = u_weight

        G.add_edge(u.item(), v.item())
        weights[v] += 1
        total_weight += 1
        out_strengths[u] += 1
        if out_strengths[u] == k:
            remaining_mask[u] = False
    return G

