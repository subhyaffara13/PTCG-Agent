
def test_yen_undirected():
    distances = yen(
        undirected_G,
        source=0,
        sink=3,
        K=4,
        directed=False,
    )
    assert_allclose(distances, [1., 4., 5., 8.])

