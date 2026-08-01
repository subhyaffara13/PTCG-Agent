
def test_greedy_source_expansion_empty_graph():
    G = nx.Graph()
    G.add_nodes_from(range(5))
    expected = {0}
    assert nx.community.greedy_source_expansion(G, source=0) == expected

