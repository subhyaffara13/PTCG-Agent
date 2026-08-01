
def undirected_G():
    G = nx.fast_gnp_random_graph(n=100, p=0.6, seed=123)
    cc = nx.closeness_centrality(G)
    return G, cc

