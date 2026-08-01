
def test_spring_layout_graph_size_heuristic(
    num_nodes, expected_method, extra_layout_kwargs
):
    """Expect 'force' layout for n < 500 and 'energy' for n >= 500"""
    G = nx.cycle_graph(num_nodes)
    # Seeded layout to compare explicit method to one determined by "auto"
    seed = 163674319

    # Compare explicit method to auto method
    expected = nx.spring_layout(
        G, method=expected_method, seed=seed, **extra_layout_kwargs
    )
    actual = nx.spring_layout(G, method="auto", seed=seed, **extra_layout_kwargs)
    assert np.allclose(list(expected.values()), list(actual.values()), atol=1e-5)

