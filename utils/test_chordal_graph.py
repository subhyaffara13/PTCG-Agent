
def test_chordal_graph():
    G = nx.complete_graph(5)
    assert nx.is_perfect_graph(G)

