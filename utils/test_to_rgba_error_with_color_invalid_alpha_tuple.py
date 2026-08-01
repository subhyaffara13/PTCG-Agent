
def test_to_rgba_error_with_color_invalid_alpha_tuple():
    with pytest.raises(ValueError, match="'alpha' must be between 0 and 1"):
        mcolors.to_rgba(('blue', 2.0))

