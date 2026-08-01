
def test_to_rgba_array_accepts_color_alpha_tuple():
    assert_array_equal(
        mcolors.to_rgba_array(('black', 0.9)),
        [[0, 0, 0, 0.9]])

