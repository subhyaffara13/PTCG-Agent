
def test_optimal_branching1():
    G = build_branching(optimal_arborescence_1)
    assert recognition.is_arborescence(G), True
    assert branchings.branching_weight(G) == 131

