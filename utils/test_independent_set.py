
def test_independent_set():
    # smoke test
    G = nx.Graph()
    assert len(maximum_independent_set(G)) == 0

