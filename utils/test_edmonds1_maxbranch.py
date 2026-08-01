
def test_edmonds1_maxbranch():
    G = G1()
    x = branchings.maximum_branching(G)
    x_ = build_branching(optimal_arborescence_1)
    assert_equal_branchings(x, x_)

