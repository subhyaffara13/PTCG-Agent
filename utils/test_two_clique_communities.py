
def test_two_clique_communities():
    test = Graph()

    # c1
    test.add_edge("a", "b")
    test.add_edge("a", "c")
    test.add_edge("b", "c")

    # connection
    test.add_edge("c", "d")

    # c2
    test.add_edge("d", "e")
    test.add_edge("d", "f")
    test.add_edge("f", "e")

    # ground truth
    ground_truth = {frozenset(["a", "c", "b"]), frozenset(["e", "d", "f"])}

    communities = asyn_fluidc(test, 2, seed=7)
    result = {frozenset(c) for c in communities}
    assert result == ground_truth

