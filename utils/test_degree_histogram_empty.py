
def test_degree_histogram_empty():
    G = nx.Graph()
    assert nx.degree_histogram(G) == []

