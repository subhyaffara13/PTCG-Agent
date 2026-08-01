
def test_trophic_levels_more_complex():
    # fmt: off
    matrix = np.array([
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ])
    # fmt: on
    G = nx.from_numpy_array(matrix, create_using=nx.DiGraph)
    d = nx.trophic_levels(G)
    expected_result = [1, 2, 3, 4]
    for ind in range(4):
        assert d[ind] == pytest.approx(expected_result[ind], abs=1e-7)

    # fmt: off
    matrix = np.array([
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ])
    # fmt: on
    G = nx.from_numpy_array(matrix, create_using=nx.DiGraph)
    d = nx.trophic_levels(G)

    expected_result = [1, 2, 2.5, 3.25]
    for ind in range(4):
        assert d[ind] == pytest.approx(expected_result[ind], abs=1e-7)

