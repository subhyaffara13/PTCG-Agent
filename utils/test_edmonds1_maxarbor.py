
def test_edmonds1_maxarbor():
    G = G1()
    x = branchings.maximum_spanning_arborescence(G)
    x_ = build_branching(optimal_arborescence_1)
    assert_equal_branchings(x, x_)

