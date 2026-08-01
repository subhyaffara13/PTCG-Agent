
def bipartite_and_clique_example(d=5, D=200, k=2):
    """
    Hard example from: Boob, Digvijay, Yu Gao, Richard Peng, Saurabh Sawlani,
    Charalampos Tsourakakis, Di Wang, and Junxing Wang. "Flowless: Extracting
    densest subgraphs without flow computations." In Proceedings of The Web
    Conference 2020, pp. 573-583. 2020.
    """
    B = nx.complete_bipartite_graph(d, D)
    H = [nx.complete_graph(d + 2) for _ in range(k)]
    G = nx.disjoint_union_all([B] + H)

    best_density = d * D / (d + D)  # of the complete bipartite graph
    correct_one_round_density = (2 * d * D + (d + 1) * (d + 2) * k) / (
        2 * d + 2 * D + 2 * k * (d + 2)
    )
    best_subgraph = set(B.nodes)
    return G, best_density, best_subgraph, correct_one_round_density

