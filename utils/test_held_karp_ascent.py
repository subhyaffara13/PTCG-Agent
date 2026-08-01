
def test_held_karp_ascent():
    """
    Test the Held-Karp relaxation with the ascent method
    """
    import networkx.algorithms.approximation.traveling_salesman as tsp

    np = pytest.importorskip("numpy")
    pytest.importorskip("scipy")

    # Adjacency matrix from page 1153 of the 1970 Held and Karp paper
    # which have been edited to be directional, but also symmetric
    G_array = np.array(
        [
            [0, 97, 60, 73, 17, 52],
            [97, 0, 41, 52, 90, 30],
            [60, 41, 0, 21, 35, 41],
            [73, 52, 21, 0, 95, 46],
            [17, 90, 35, 95, 0, 81],
            [52, 30, 41, 46, 81, 0],
        ]
    )

    solution_edges = [(1, 3), (2, 4), (3, 2), (4, 0), (5, 1), (0, 5)]

    G = nx.from_numpy_array(G_array, create_using=nx.DiGraph)
    opt_hk, z_star = tsp.held_karp_ascent(G)

    # Check that the optimal weights are the same
    assert round(opt_hk, 2) == 207.00
    # Check that the z_stars are the same
    solution = nx.DiGraph()
    solution.add_edges_from(solution_edges)
    # Use undirected edges for `edges_equal` because the graph is symmetric.
    assert nx.utils.edges_equal(z_star.edges, solution.edges)

