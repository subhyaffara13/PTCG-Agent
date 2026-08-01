
def test_to_rgba_accepts_color_alpha_tuple(rgba_alpha):
    assert mcolors.to_rgba(rgba_alpha) == (1, 1, 1, 0.5)

