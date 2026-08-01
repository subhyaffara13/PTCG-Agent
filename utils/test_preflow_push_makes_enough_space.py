
def test_preflow_push_makes_enough_space():
    # From ticket #1542
    G = nx.DiGraph()
    nx.add_path(G, [0, 1, 3], capacity=1)
    nx.add_path(G, [1, 2, 3], capacity=1)
    R = preflow_push(G, 0, 3, value_only=False)
    assert R.graph["flow_value"] == 1

