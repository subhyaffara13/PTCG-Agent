
def test_ascent_fractional_solution():
    """
    Test the ascent method using a modified version of Figure 2 on page 1140
    in 'The Traveling Salesman Problem and Minimum Spanning Trees' by Held and
    Karp
    """
    import networkx.algorithms.approximation.traveling_salesman as tsp

    np = pytest.importorskip("numpy")
    pytest.importorskip("scipy")

    # This version of Figure 2 has all of the edge weights multiplied by 100
    # and is a complete directed graph with infinite edge weights for the
    # edges not listed in the original graph
    G_array = np.array(
        [
            [0, 100, 100, 100000, 100000, 1],
            [100, 0, 100, 100000, 1, 100000],
            [100, 100, 0, 1, 100000, 100000],
            [100000, 100000, 1, 0, 100, 100],
            [100000, 1, 100000, 100, 0, 100],
            [1, 100000, 100000, 100, 100, 0],
        ]
    )

    solution_z_star = {
        (0, 1): 5 / 12,
        (0, 2): 5 / 12,
        (0, 5): 5 / 6,
        (1, 0): 5 / 12,
        (1, 2): 1 / 3,
        (1, 4): 5 / 6,
        (2, 0): 5 / 12,
        (2, 1): 1 / 3,
        (2, 3): 5 / 6,
        (3, 2): 5 / 6,
        (3, 4): 1 / 3,
        (3, 5): 1 / 2,
        (4, 1): 5 / 6,
        (4, 3): 1 / 3,
        (4, 5): 1 / 2,
        (5, 0): 5 / 6,
        (5, 3): 1 / 2,
        (5, 4): 1 / 2,
    }

    G = nx.from_numpy_array(G_array, create_using=nx.DiGraph)
    opt_hk, z_star = tsp.held_karp_ascent(G)

    # Check that the optimal weights are the same
    assert round(opt_hk, 2) == 303.00
    # Check that the z_stars are the same
    assert {key: round(z_star[key], 4) for key in z_star} == {
        key: round(solution_z_star[key], 4) for key in solution_z_star
    }

