
def test_asadpour_integral_held_karp():
    """
    This test uses an integral held karp solution and the held karp function
    will return a graph rather than a dict, bypassing most of the asadpour
    algorithm.

    At first glance, this test probably doesn't look like it ensures that we
    skip the rest of the asadpour algorithm, but it does. We are not fixing a
    see for the random number generator, so if we sample any spanning trees
    the approximation would be different basically every time this test is
    executed but it is not since held karp is deterministic and we do not
    reach the portion of the code with the dependence on random numbers.
    """
    np = pytest.importorskip("numpy")

    G_array = np.array(
        [
            [0, 26, 63, 59, 69, 31, 41],
            [62, 0, 91, 53, 75, 87, 47],
            [47, 82, 0, 90, 15, 9, 18],
            [68, 19, 5, 0, 58, 34, 93],
            [11, 58, 53, 55, 0, 61, 79],
            [88, 75, 13, 76, 98, 0, 40],
            [41, 61, 55, 88, 46, 45, 0],
        ]
    )

    G = nx.from_numpy_array(G_array, create_using=nx.DiGraph)

    for _ in range(2):
        tour = nx_app.traveling_salesman_problem(G, method=nx_app.asadpour_atsp)

        assert [1, 3, 2, 5, 2, 6, 4, 0, 1] == tour

