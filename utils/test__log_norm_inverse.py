
def test_LogNorm_inverse():
    """
    Test that lists work, and that the inverse works
    """
    norm = mcolors.LogNorm(vmin=0.1, vmax=10)
    assert_array_almost_equal(norm([0.5, 0.4]), [0.349485, 0.30103])
    assert_array_almost_equal([0.5, 0.4], norm.inverse([0.349485, 0.30103]))
    assert_array_almost_equal(norm(0.4), [0.30103])
    assert_array_almost_equal([0.4], norm.inverse([0.30103]))

