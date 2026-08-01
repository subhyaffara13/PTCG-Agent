
def test_generate_random_paths_source_not_in_G(source):
    pytest.importorskip("numpy")
    G = nx.complete_graph(5)
    # No exception at generator construction time
    path_gen = nx.generate_random_paths(G, sample_size=3, source=source)
    with pytest.raises(nx.NodeNotFound, match="Initial node.*not in G"):
        next(path_gen)

