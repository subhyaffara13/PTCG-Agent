
def test_graph_could_be_isomorphic_variants_deprecated():
    G1 = nx.Graph([(1, 2), (1, 3), (1, 5), (2, 3)])
    G2 = nx.Graph([(10, 20), (20, 30), (10, 30), (10, 50)])
    with pytest.deprecated_call():  # graph_could_be_isomorphic
        result = nx.isomorphism.isomorph.graph_could_be_isomorphic(G1, G2)
    assert nx.could_be_isomorphic(G1, G2) == result
    with pytest.deprecated_call():  # fast_graph_could_be_isomorphic
        result = nx.isomorphism.isomorph.fast_graph_could_be_isomorphic(G1, G2)
    assert nx.fast_could_be_isomorphic(G1, G2) == result
    with pytest.deprecated_call():
        result = nx.isomorphism.isomorph.faster_graph_could_be_isomorphic(G1, G2)
    assert nx.faster_could_be_isomorphic(G1, G2) == result

