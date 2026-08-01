
def test_from_graph6_invariant_to_trailing_newline():
    """See gh-7557"""
    G = nx.from_graph6_bytes(b">>graph6<<P~~~~~~~~~~~~~~~~~~~~~~{\n")
    H = nx.from_graph6_bytes(b">>graph6<<P~~~~~~~~~~~~~~~~~~~~~~{")
    assert nx.utils.graphs_equal(G, H)

