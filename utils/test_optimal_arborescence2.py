
def test_optimal_arborescence2():
    G = build_branching(optimal_arborescence_2)
    assert recognition.is_arborescence(G), True
    assert branchings.branching_weight(G) == 51

