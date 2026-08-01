
def test_greedy_max1():
    # Standard test.
    #
    G = G1()
    B = branchings.greedy_branching(G)
    # There are only two possible greedy branchings. The sorting is such
    # that it should equal the second suboptimal branching: 1b.
    B_ = build_branching(greedy_subopt_branching_1b)
    assert_equal_branchings(B, B_)

