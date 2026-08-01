
def test_monomorphism_iter1():
    g1 = nx.DiGraph(["AB", "BC", "CA"])
    g2 = nx.DiGraph(["XY", "YZ"])
    gm12 = iso.DiGraphMatcher(g1, g2)
    x = list(gm12.subgraph_monomorphisms_iter())
    assert {"A": "X", "B": "Y", "C": "Z"} in x
    assert {"A": "Y", "B": "Z", "C": "X"} in x
    assert {"A": "Z", "B": "X", "C": "Y"} in x
    assert len(x) == 3
    gm21 = iso.DiGraphMatcher(g2, g1)
    # Check if StopIteration exception returns False
    assert not gm21.subgraph_is_monomorphic()

