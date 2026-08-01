
def test_union_multigraph():
    G = nx.MultiGraph()
    G.add_edge(1, 2, key=0)
    G.add_edge(1, 2, key=1)
    H = nx.MultiGraph()
    H.add_edge(3, 4, key=0)
    H.add_edge(3, 4, key=1)
    GH = nx.union(G, H)
    assert set(GH) == set(G) | set(H)
    assert set(GH.edges(keys=True)) == set(G.edges(keys=True)) | set(H.edges(keys=True))

