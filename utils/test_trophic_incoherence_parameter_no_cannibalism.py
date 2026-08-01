
def test_trophic_incoherence_parameter_no_cannibalism():
    matrix_a = np.array([[0, 1], [0, 0]])
    G = nx.from_numpy_array(matrix_a, create_using=nx.DiGraph)
    q = nx.trophic_incoherence_parameter(G, cannibalism=False)
    assert q == pytest.approx(0, abs=1e-7)

    # fmt: off
    matrix_b = np.array([
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ])
    # fmt: on
    G = nx.from_numpy_array(matrix_b, create_using=nx.DiGraph)
    q = nx.trophic_incoherence_parameter(G, cannibalism=False)
    assert q == pytest.approx(np.std([1, 1.5, 0.5, 0.75, 1.25]), abs=1e-7)

    # fmt: off
    matrix_c = np.array([
        [0, 1, 1, 0],
        [0, 1, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 1]
    ])
    # fmt: on
    G = nx.from_numpy_array(matrix_c, create_using=nx.DiGraph)
    q = nx.trophic_incoherence_parameter(G, cannibalism=False)
    # Ignore the -link
    assert q == pytest.approx(np.std([1, 1.5, 0.5, 0.75, 1.25]), abs=1e-7)

    # no self-loops case
    # fmt: off
    matrix_d = np.array([
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [0, 0, 0, 0]
    ])
    # fmt: on
    G = nx.from_numpy_array(matrix_d, create_using=nx.DiGraph)
    q = nx.trophic_incoherence_parameter(G, cannibalism=False)
    # Ignore the -link
    assert q == pytest.approx(np.std([1, 1.5, 0.5, 0.75, 1.25]), abs=1e-7)

