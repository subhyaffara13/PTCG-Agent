
def test_asyn_fluidc_max_iter():
    """Check that setting `max_iter` stops the algorithm early."""
    test = nx.barbell_graph(3, 2)

    c1 = asyn_fluidc(test, 2, max_iter=1, seed=42)
    c2 = asyn_fluidc(test, 2, max_iter=100, seed=42)
    assert {map(frozenset, c1)} != {map(frozenset, c2)}

