
def test_to_rgba_array_none_color_with_alpha_param():
    # effective alpha for color "none" must always be 0 to achieve a vanishing color
    # even explicit alpha must be ignored
    c = ["blue", "none"]
    alpha = [1, 1]
    assert_array_equal(
        to_rgba_array(c, alpha), [[0., 0., 1., 1.], [0., 0., 0., 0.]]
    )

