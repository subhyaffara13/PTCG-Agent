
def test_greedy_max2():
    # Different default weight.
    #
    G = G1()
    del G[1][0][0]["weight"]
    B = branchings.greedy_branching(G, default=6)
    # Chosen so that edge (3,0,5) is not selected and (1,0,6) is instead.

    edges = [
        (1, 0, 6),
        (1, 5, 13),
        (7, 6, 15),
        (2, 1, 17),
        (3, 4, 17),
        (8, 7, 18),
        (2, 3, 21),
        (6, 2, 21),
    ]
    B_ = build_branching(edges)
    assert_equal_branchings(B, B_)

