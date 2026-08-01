
def test_bivar_getitem():
    """Test __getitem__  on BivarColormap"""
    xA = ([.0, .25, .5, .75, 1., -1, 2], [.5]*7)
    xB = ([.5]*7, [.0, .25, .5, .75, 1., -1, 2])

    cmaps = mpl.bivar_colormaps['BiPeak']
    assert_array_equal(cmaps(xA), cmaps[0](xA[0]))
    assert_array_equal(cmaps(xB), cmaps[1](xB[1]))

    cmaps = cmaps.with_extremes(shape='ignore')
    assert_array_equal(cmaps(xA), cmaps[0](xA[0]))
    assert_array_equal(cmaps(xB), cmaps[1](xB[1]))

    xA = ([.0, .25, .5, .75, 1., -1, 2], [.0]*7)
    xB = ([.0]*7, [.0, .25, .5, .75, 1., -1, 2])
    cmaps = mpl.bivar_colormaps['BiOrangeBlue']
    assert_array_equal(cmaps(xA), cmaps[0](xA[0]))
    assert_array_equal(cmaps(xB), cmaps[1](xB[1]))

    cmaps = cmaps.with_extremes(shape='ignore')
    assert_array_equal(cmaps(xA), cmaps[0](xA[0]))
    assert_array_equal(cmaps(xB), cmaps[1](xB[1]))

