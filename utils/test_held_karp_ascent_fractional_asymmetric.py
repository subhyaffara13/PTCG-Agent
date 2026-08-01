
def test_held_karp_ascent_fractional_asymmetric():
    """
    Tests the ascent method using a truly asymmetric graph with a fractional
    solution for which the solution has been brute forced
    """
    import networkx.algorithms.approximation.traveling_salesman as tsp

    np = pytest.importorskip("numpy")
    pytest.importorskip("scipy")

    G_array = np.array(
        [
            [0, 100, 150, 100000, 100000, 1],
            [150, 0, 100, 100000, 1, 100000],
            [100, 150, 0, 1, 100000, 100000],
            [100000, 100000, 1, 0, 150, 100],
            [100000, 2, 100000, 100, 0, 150],
            [2, 100000, 100000, 150, 100, 0],
        ]
    )

    solution_z_star = {
        (0, 1): 5 / 12,
        (0, 2): 5 / 12,
        (0, 5): 5 / 6,
        (1, 0): 5 / 12,
        (1, 2): 5 / 12,
        (1, 4): 5 / 6,
        (2, 0): 5 / 12,
        (2, 1): 5 / 12,
        (2, 3): 5 / 6,
        (3, 2): 5 / 6,
        (3, 4): 5 / 12,
        (3, 5): 5 / 12,
        (4, 1): 5 / 6,
        (4, 3): 5 / 12,
        (4, 5): 5 / 12,
        (5, 0): 5 / 6,
        (5, 3): 5 / 12,
        (5, 4): 5 / 12,
    }

    G = nx.from_numpy_array(G_array, create_using=nx.DiGraph)
    opt_hk, z_star = tsp.held_karp_ascent(G)

    # Check that the optimal weights are the same
    assert round(opt_hk, 2) == 304.00
    # Check that the z_stars are the same
    assert {key: round(z_star[key], 4) for key in z_star} == {
        key: round(solution_z_star[key], 4) for key in solution_z_star
    }

