
def test_topological_generations_empty():
    G = nx.DiGraph()
    assert list(nx.topological_generations(G)) == []

