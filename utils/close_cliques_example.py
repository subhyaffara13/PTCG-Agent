
def close_cliques_example(d=12, D=300, h=24, k=2):
    """
    Hard example from Harb, Elfarouk, Kent Quanrud, and Chandra Chekuri.
    "Faster and scalable algorithms for densest subgraph and decomposition."
    Advances in Neural Information Processing Systems 35 (2022): 26966-26979.
    """
    Kh = nx.complete_graph(h)
    KdD = nx.complete_bipartite_graph(d, D)
    G = nx.disjoint_union_all([KdD] + [Kh for _ in range(k)])
    best_density = d * D / (d + D)  # of the complete bipartite graph
    return G, best_density, set(KdD.nodes)

