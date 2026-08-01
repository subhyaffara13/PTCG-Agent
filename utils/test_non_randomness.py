
def test_non_randomness(k, weight, expected):
    G = nx.karate_club_graph()
    np.testing.assert_almost_equal(
        nx.non_randomness(G, k, weight)[0], expected, decimal=2
    )

