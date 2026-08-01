
def test_even_cycle():
    G = nx.cycle_graph(6)  # Even cycle is perfect
    assert nx.is_perfect_graph(G)

