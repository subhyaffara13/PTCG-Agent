
def test_to_rgba_array_accepts_color_alpha_tuple_with_multiple_colors():
    color_array = np.array([[1., 1., 1., 1.], [0., 0., 1., 0.]])
    assert_array_equal(
        mcolors.to_rgba_array((color_array, 0.2)),
        [[1., 1., 1., 0.2], [0., 0., 1., 0.2]])

    color_sequence = [[1., 1., 1., 1.], [0., 0., 1., 0.]]
    assert_array_equal(
        mcolors.to_rgba_array((color_sequence, 0.4)),
        [[1., 1., 1., 0.4], [0., 0., 1., 0.4]])

