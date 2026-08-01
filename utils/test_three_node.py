
def test_three_node(e1, e2, isomorphic, subgraph_is_isomorphic):
    """Test some edge cases distilled from arbitrary search of the input space."""
    G1 = nx.DiGraph(e1)
    G2 = nx.DiGraph(e2)
    gm = iso.DiGraphMatcher(G1, G2)
    assert gm.is_isomorphic() == isomorphic
    assert gm.subgraph_is_isomorphic() == subgraph_is_isomorphic

