
def test_greedy_suboptimal_branching1b():
    G = build_branching(greedy_subopt_branching_1b)
    assert recognition.is_arborescence(G), True
    assert branchings.branching_weight(G) == 127

