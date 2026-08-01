
def test_greedy_branching_kwarg_kind():
    G = G1()
    with pytest.raises(nx.NetworkXException, match="Unknown value for `kind`."):
        B = branchings.greedy_branching(G, kind="lol")

