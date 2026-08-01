
def test_could_be_isomorphic_individual_vs_combined_dt():
    """A test case where G and H have identical degree and triangle distributions,
    but are different when compared together"""
    G = nx.Graph([(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (3, 4), (4, 5), (4, 6)])
    H = G.copy()
    # Modify graphs to produce different clique distributions
    G.add_edge(0, 7)
    H.add_edge(4, 7)
    assert nx.could_be_isomorphic(G, H, properties="d")
    assert nx.could_be_isomorphic(G, H, properties="t")
    assert not nx.could_be_isomorphic(G, H, properties="dt")
    assert not nx.could_be_isomorphic(G, H, properties="c")

