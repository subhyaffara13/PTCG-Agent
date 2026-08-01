
def test_petersen_seed():
    # Actual coefficient is 0
    G = nx.petersen_graph()
    assert average_clustering(G, trials=len(G) // 2, seed=1) == nx.average_clustering(G)

