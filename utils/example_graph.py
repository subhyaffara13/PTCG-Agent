
def example_graph():
    G = nx.Graph()
    G.add_weighted_edges_from([(1, 2, 3.0), (2, 3, 27.0), (3, 4, 3.0)])
    return G

