
def test_bipartite_layout_default_nodes():
    G = nx.complete_bipartite_graph(3, 3)
    pos = nx.bipartite_layout(G)  # no nodes specified
    # X coords of nodes should be the same within the bipartite sets
    for nodeset in nx.bipartite.sets(G):
        xs = [pos[k][0] for k in nodeset]
        assert all(x == pytest.approx(xs[0]) for x in xs)

