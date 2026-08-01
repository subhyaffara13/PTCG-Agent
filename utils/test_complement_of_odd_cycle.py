
def test_complement_of_odd_cycle():
    G = nx.cycle_graph(7)
    GC = nx.complement(G)
    assert not nx.is_perfect_graph(GC)

