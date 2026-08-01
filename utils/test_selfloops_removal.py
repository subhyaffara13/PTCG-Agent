
def test_selfloops_removal(graph_type):
    G = nx.complete_graph(3, create_using=graph_type)
    G.add_edge(0, 0)
    G.remove_edges_from(nx.selfloop_edges(G, keys=True))
    G.add_edge(0, 0)
    G.remove_edges_from(nx.selfloop_edges(G, data=True))
    G.add_edge(0, 0)
    G.remove_edges_from(nx.selfloop_edges(G, keys=True, data=True))

