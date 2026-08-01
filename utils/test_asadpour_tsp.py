
def test_asadpour_tsp():
    """
    Test the complete asadpour tsp algorithm with the fractional, symmetric
    Held Karp solution. This test also uses an incomplete graph as input.
    """
    # This version of Figure 2 has all of the edge weights multiplied by 100
    # and the 0 weight edges have a weight of 1.
    pytest.importorskip("numpy")
    pytest.importorskip("scipy")

    edge_list = [
        (0, 1, 100),
        (0, 2, 100),
        (0, 5, 1),
        (1, 2, 100),
        (1, 4, 1),
        (2, 3, 1),
        (3, 4, 100),
        (3, 5, 100),
        (4, 5, 100),
        (1, 0, 100),
        (2, 0, 100),
        (5, 0, 1),
        (2, 1, 100),
        (4, 1, 1),
        (3, 2, 1),
        (4, 3, 100),
        (5, 3, 100),
        (5, 4, 100),
    ]

    G = nx.DiGraph()
    G.add_weighted_edges_from(edge_list)

    tour = nx_app.traveling_salesman_problem(
        G, weight="weight", method=nx_app.asadpour_atsp, seed=19
    )

    # Check that the returned list is a valid tour. Because this is an
    # incomplete graph, the conditions are not as strict. We need the tour to
    #
    #   Start and end at the same node
    #   Pass through every vertex at least once
    #   Have a total cost at most ln(6) / ln(ln(6)) = 3.0723 times the optimal
    #
    # For the second condition it is possible to have the tour pass through the
    # same vertex more then. Imagine that the tour on the complete version takes
    # an edge not in the original graph. In the output this is substituted with
    # the shortest path between those vertices, allowing vertices to appear more
    # than once.
    #
    # Even though we are using a fixed seed, multiple tours have been known to
    # be returned. The first two are from the original development of this test,
    # and the third one from issue #5913 on GitHub. If other tours are returned,
    # add it on the list of expected tours.
    expected_tours = [
        [1, 4, 5, 0, 2, 3, 2, 1],
        [3, 2, 0, 1, 4, 5, 3],
        [3, 2, 1, 0, 5, 4, 3],
    ]

    assert tour in expected_tours

