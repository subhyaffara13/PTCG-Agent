
def test_karate_directed():
    G = nx.karate_club_graph().to_directed()
    _check_edge_connectivity(G)

