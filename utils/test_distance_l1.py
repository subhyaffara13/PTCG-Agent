
def test_distance_l1():
    with pytest.deprecated_call(match="1.20.0"):
        assert_almost_equal(minkowski_distance([0, 0], [1, 1], 1), 2)

