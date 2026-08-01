
def test_failed_conversions():
    with pytest.raises(ValueError):
        mcolors.to_rgba('5')
    with pytest.raises(ValueError):
        mcolors.to_rgba('-1')
    with pytest.raises(ValueError):
        mcolors.to_rgba('nan')
    with pytest.raises(ValueError):
        mcolors.to_rgba('unknown_color')
    with pytest.raises(ValueError):
        # Gray must be a string to distinguish 3-4 grays from RGB or RGBA.
        mcolors.to_rgba(0.4)

