
def test_two_nodes():
    test = Graph()

    test.add_edge("a", "b")

    # ground truth
    ground_truth = {frozenset(["a"]), frozenset(["b"])}

    communities = asyn_fluidc(test, 2)
    result = {frozenset(c) for c in communities}
    assert result == ground_truth

