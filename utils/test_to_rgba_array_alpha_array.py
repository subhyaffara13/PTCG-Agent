
def test_to_rgba_array_alpha_array():
    with pytest.raises(ValueError, match="The number of colors must match"):
        mcolors.to_rgba_array(np.ones((5, 3), float), alpha=np.ones((2,)))
    alpha = [0.5, 0.6]
    c = mcolors.to_rgba_array(np.ones((2, 3), float), alpha=alpha)
    assert_array_equal(c[:, 3], alpha)
    c = mcolors.to_rgba_array(['r', 'g'], alpha=alpha)
    assert_array_equal(c[:, 3], alpha)

