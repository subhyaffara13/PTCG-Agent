
def test_spectral_bipartition():
    pytest.importorskip("scipy")
    G = nx.barbell_graph(3, 0)
    split = nx.community.spectral_modularity_bipartition(G)
    soln = ({3, 4, 5}, {0, 1, 2})
    assert set(map(frozenset, split)) == set(map(frozenset, soln))

