
def test_non_repeated_cuts():
    # The algorithm was repeating the cut {0, 1} for the giant biconnected
    # component of the Karate club graph.
    K = nx.karate_club_graph()
    bcc = max(list(nx.biconnected_components(K)), key=len)
    G = K.subgraph(bcc)
    solution = [{32, 33}, {2, 33}, {0, 3}, {0, 1}, {29, 33}]
    cuts = list(nx.all_node_cuts(G))
    assert len(solution) == len(cuts)
    for cut in cuts:
        assert cut in solution

