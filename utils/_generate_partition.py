
def _generate_partition(G, cuts, k):
    def has_nbrs_in_partition(G, node, partition):
        return any(n in partition for n in G[node])

    components = []
    n_in_cuts = {n for cut in cuts for n in cut}
    nodes = {n for n, d in G.degree() if d > k} - n_in_cuts
    H = G.subgraph(nodes)
    for cc in map(set, nx.connected_components(H)):
        component = cc | {n for n in n_in_cuts if has_nbrs_in_partition(G, n, cc)}
        if len(component) < G.order():
            components.append(component)
    yield from _consolidate(components, k + 1)

