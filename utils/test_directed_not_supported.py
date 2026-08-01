
def test_directed_not_supported():
    with pytest.raises(nx.NetworkXNotImplemented):
        # not supported for directed graphs
        test = nx.DiGraph()
        test.add_edge("a", "b")
        test.add_edge("a", "c")
        test.add_edge("b", "d")
        result = nx.community.label_propagation_communities(test)

