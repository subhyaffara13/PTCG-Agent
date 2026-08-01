
def test_edmonds2_maxarbor():
    G = G2()
    x = branchings.maximum_spanning_arborescence(G)
    x_ = build_branching(optimal_arborescence_2)
    assert_equal_branchings(x, x_)

