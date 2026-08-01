
def test_ra_clustering_davis():
    G = nx.davis_southern_women_graph()
    cc4 = round(bipartite.robins_alexander_clustering(G), 3)
    assert cc4 == 0.468

