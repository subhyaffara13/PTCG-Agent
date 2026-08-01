
def test_bivar_eq():
    """
    Tests equality between multivariate colormaps
    """
    cmap_0 = mpl.bivar_colormaps['BiPeak']

    cmap_1 = mpl.bivar_colormaps['BiPeak']
    assert (cmap_0 == cmap_1) is True

    cmap_1 = mpl.multivar_colormaps['2VarAddA']
    assert (cmap_0 == cmap_1) is False

    cmap_1 = mpl.bivar_colormaps['BiCone']
    assert (cmap_0 == cmap_1) is False

    cmap_1 = mpl.bivar_colormaps['BiPeak']
    cmap_1 = cmap_1.with_extremes(bad='k')
    assert (cmap_0 == cmap_1) is False

    cmap_1 = mpl.bivar_colormaps['BiPeak']
    cmap_1 = cmap_1.with_extremes(outside='k')
    assert (cmap_0 == cmap_1) is False

    cmap_1 = mpl.bivar_colormaps['BiPeak']
    cmap_1._init()
    cmap_1._lut *= 0.5
    assert (cmap_0 == cmap_1) is False

    cmap_1 = mpl.bivar_colormaps['BiPeak']
    cmap_1 = cmap_1.with_extremes(shape='ignore')
    assert (cmap_0 == cmap_1) is False

