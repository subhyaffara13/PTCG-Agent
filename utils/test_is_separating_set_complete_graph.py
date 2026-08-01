
def test_is_separating_set_complete_graph():
    G = nx.complete_graph(5)
    assert _is_separating_set(G, {0, 1, 2, 3})

