
def test_unconnected_communities():
    test = nx.Graph()
    # community 1
    test.add_edge("a", "c")
    test.add_edge("a", "d")
    test.add_edge("d", "c")
    # community 2
    test.add_edge("b", "e")
    test.add_edge("e", "f")
    test.add_edge("f", "b")

    # The expected communities are:
    ground_truth = {frozenset(["a", "c", "d"]), frozenset(["b", "e", "f"])}

    communities = nx.community.label_propagation_communities(test)
    result = {frozenset(c) for c in communities}
    assert result == ground_truth

