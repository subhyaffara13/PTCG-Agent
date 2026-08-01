
def test_cycle_graph():
    G = nx.cycle_graph(5)
    solution = [{0, 2}, {0, 3}, {1, 3}, {1, 4}, {2, 4}]
    cuts = list(nx.all_node_cuts(G))
    assert len(solution) == len(cuts)
    for cut in cuts:
        assert cut in solution

