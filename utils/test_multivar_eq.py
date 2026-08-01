
def test_multivar_eq():
    """
    Tests equality between multivariate colormaps
    """
    cmap_0 = mpl.multivar_colormaps['2VarAddA']

    cmap_1 = mpl.multivar_colormaps['2VarAddA']
    assert (cmap_0 == cmap_1) is True

    cmap_1 = mpl.bivar_colormaps['BiPeak']
    assert (cmap_0 == cmap_1) is False

    cmap_1 = mpl.colors.MultivarColormap([cmap_0[0]]*2,
                                         'sRGB_add')
    assert (cmap_0 == cmap_1) is False

    cmap_1 = mpl.multivar_colormaps['3VarAddA']
    assert (cmap_0 == cmap_1) is False

    cmap_1 = mpl.multivar_colormaps['2VarAddA']
    cmap_1 = cmap_1.with_extremes(bad='k')
    assert (cmap_0 == cmap_1) is False

    cmap_1 = mpl.multivar_colormaps['2VarAddA']
    cmap_1 = mpl.colors.MultivarColormap(cmap_1[:], 'sRGB_sub')
    assert (cmap_0 == cmap_1) is False

