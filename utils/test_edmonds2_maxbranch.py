
def test_edmonds2_maxbranch():
    G = G2()
    x = branchings.maximum_branching(G)
    x_ = build_branching(optimal_branching_2a)
    assert_equal_branchings(x, x_)

