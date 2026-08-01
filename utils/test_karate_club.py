
def test_karate_club():
    pytest.importorskip("scipy")
    G = nx.karate_club_graph()
    MrHi = {v for v, club in G.nodes.data("club") if club == "Mr. Hi"}
    Officer = {v for v, club in G.nodes.data("club") if club == "Officer"}
    split = nx.community.spectral_modularity_bipartition(G)

    # spectral method misplaces member 8
    MrHi.remove(8)
    Officer.add(8)
    soln = (MrHi, Officer)
    assert set(map(frozenset, split)) == set(map(frozenset, soln))

