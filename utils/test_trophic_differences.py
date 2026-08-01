
def test_trophic_differences():
    matrix_a = np.array([[0, 1], [0, 0]])
    G = nx.from_numpy_array(matrix_a, create_using=nx.DiGraph)
    diffs = nx.trophic_differences(G)
    assert diffs[(0, 1)] == pytest.approx(1, abs=1e-7)

    # fmt: off
    matrix_b = np.array([
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ])
    # fmt: on
    G = nx.from_numpy_array(matrix_b, create_using=nx.DiGraph)
    diffs = nx.trophic_differences(G)

    assert diffs[(0, 1)] == pytest.approx(1, abs=1e-7)
    assert diffs[(0, 2)] == pytest.approx(1.5, abs=1e-7)
    assert diffs[(1, 2)] == pytest.approx(0.5, abs=1e-7)
    assert diffs[(1, 3)] == pytest.approx(1.25, abs=1e-7)
    assert diffs[(2, 3)] == pytest.approx(0.75, abs=1e-7)

