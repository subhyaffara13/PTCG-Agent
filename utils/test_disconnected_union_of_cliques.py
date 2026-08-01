
def test_disconnected_union_of_cliques():
    G = nx.disjoint_union(nx.complete_graph(3), nx.complete_graph(4))
    assert nx.is_perfect_graph(G)

