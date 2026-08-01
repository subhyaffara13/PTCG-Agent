
def test_generate_random_paths_with_isolated_nodes():
    pytest.importorskip("numpy")
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2])
    G.add_edge(0, 1)

    # Connected source node
    paths = list(nx.generate_random_paths(G, 2, path_length=2, source=0, seed=42))
    assert len(paths) == 2
    assert all(len(path) == 3 for path in paths)
    assert all(path[0] == 0 for path in paths)

    # Isolated source node
    path_gen = nx.generate_random_paths(G, 2, path_length=2, source=2, seed=42)
    with pytest.raises(ValueError, match="probabilities contain NaN"):
        list(path_gen)

    # Random source that might pick isolated node
    path_gen = nx.generate_random_paths(G, 2, path_length=2, seed=42)
    with pytest.raises(ValueError, match="probabilities contain NaN"):
        list(path_gen)

