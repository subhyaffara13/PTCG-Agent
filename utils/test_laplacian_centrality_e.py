
def test_laplacian_centrality_E():
    E = nx.Graph()
    E.add_weighted_edges_from(
        [(0, 1, 4), (4, 5, 1), (0, 2, 2), (2, 1, 1), (1, 3, 2), (1, 4, 2)]
    )
    d = nx.laplacian_centrality(E)
    exact = {
        0: 0.700000,
        1: 0.900000,
        2: 0.280000,
        3: 0.220000,
        4: 0.260000,
        5: 0.040000,
    }

    for n, dc in d.items():
        assert exact[n] == pytest.approx(dc, abs=1e-7)

    # Check not normalized
    full_energy = 200
    dnn = nx.laplacian_centrality(E, normalized=False)
    for n, dc in dnn.items():
        assert exact[n] * full_energy == pytest.approx(dc, abs=1e-7)

    # Check unweighted not-normalized version
    duw_nn = nx.laplacian_centrality(E, normalized=False, weight=None)
    exact_uw_nn = {
        0: 18,
        1: 34,
        2: 18,
        3: 10,
        4: 16,
        5: 6,
    }
    for n, dc in duw_nn.items():
        assert exact_uw_nn[n] == pytest.approx(dc, abs=1e-7)

    # Check unweighted version
    duw = nx.laplacian_centrality(E, weight=None)
    full_energy = 42
    for n, dc in duw.items():
        assert exact_uw_nn[n] / full_energy == pytest.approx(dc, abs=1e-7)

