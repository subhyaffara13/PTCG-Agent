
def test_colorizer_multinorm_explicit():

    with pytest.raises(ValueError, match="MultiNorm must be assigned"):
        ca = mcolorizer.Colorizer('BiOrangeBlue', 'linear')

    with pytest.raises(TypeError,
                       match=("'norm' must be an instance of matplotlib.colors.Norm"
                              ", str or None, not a list")):
        ca = mcolorizer.Colorizer('viridis', ['linear', 'linear'])

    with pytest.raises(ValueError,
                       match=("Invalid norm for multivariate colormap with 2 inputs")):
        ca = mcolorizer.Colorizer('BiOrangeBlue', ['linear', 'linear', 'log'])

    # valid explicit construction
    ca = mcolorizer.Colorizer('BiOrangeBlue', [mcolors.Normalize(), 'log'])
    ca.vmin = (0, 0.01)
    ca.vmax = (1, 1)

    # test call with two single values
    data = [0.1, 0.2]
    res = (0.098039, 0.374510, 0.65098, 1.)
    assert_array_almost_equal(ca.to_rgba(data), res)

