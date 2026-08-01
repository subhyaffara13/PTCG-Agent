
def test_to_rgba_array_2tuple_str():
    expected = np.array([[0, 0, 0, 1], [1, 1, 1, 1]])
    assert_array_equal(mcolors.to_rgba_array(("k", "w")), expected)

