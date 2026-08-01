
def test_single_node():
    test = Graph()

    test.add_node("a")

    # ground truth
    ground_truth = {frozenset(["a"])}

    communities = asyn_fluidc(test, 1)
    result = {frozenset(c) for c in communities}
    assert result == ground_truth

