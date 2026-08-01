
def test_ssp_multigraph():
    with pytest.raises(nx.NetworkXNotImplemented):
        G = nx.MultiGraph()
        nx.add_path(G, [1, 2, 3])
        list(nx.shortest_simple_paths(G, 1, 4))

