
def _four_cycles(G):
    # Also see `square_clustering` which counts squares in a similar way
    cycles = 0
    seen = set()
    G_adj = G._adj
    for v in G:
        seen.add(v)
        v_neighbors = set(G_adj[v])
        if len(v_neighbors) < 2:
            # Can't form a square without at least two neighbors
            continue
        two_hop_neighbors = set().union(*(G_adj[u] for u in v_neighbors))
        two_hop_neighbors -= seen
        for x in two_hop_neighbors:
            p2 = len(v_neighbors.intersection(G_adj[x]))
            cycles += p2 * (p2 - 1)
    return cycles / 4

