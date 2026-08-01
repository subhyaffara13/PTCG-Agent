
def multigraph_test_graph():
    G = nx.MultiGraph()
    G.add_edge(1, 2, weight=7)
    G.add_edge(1, 2, weight=70)
    return G

