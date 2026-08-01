
def test_odd_cycle():
    G = nx.cycle_graph(5)  # Induced odd cycle
    assert not nx.is_perfect_graph(G)

