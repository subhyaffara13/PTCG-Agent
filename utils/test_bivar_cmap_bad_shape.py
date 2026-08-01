
def test_bivar_cmap_bad_shape():
    """
    Tests calling a bivariate colormap with integer values
    """
    cmap = mpl.bivar_colormaps['BiCone']
    _ = cmap.lut
    with pytest.raises(ValueError,
                       match="is not a valid value for shape"):
        cmap.with_extremes(shape='bad_shape')

    with pytest.raises(ValueError,
                       match="is not a valid value for shape"):
        mpl.colors.BivarColormapFromImage(np.ones((3, 3, 4)),
                                          shape='bad_shape')

