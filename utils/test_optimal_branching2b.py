
def test_optimal_branching2b():
    G = build_branching(optimal_branching_2b)
    assert recognition.is_arborescence(G), True
    assert branchings.branching_weight(G) == 53

