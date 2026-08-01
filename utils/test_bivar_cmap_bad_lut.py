
def test_bivar_cmap_bad_lut():
    """
    Tests calling a bivariate colormap with integer values
    """
    with pytest.raises(ValueError,
                       match="The lut must be an array of shape"):
        cmap = mpl.colors.BivarColormapFromImage(np.ones((3, 3, 5)))

