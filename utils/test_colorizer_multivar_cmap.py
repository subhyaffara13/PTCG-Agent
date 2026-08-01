
def test_colorizer_multivar_cmap():
    ca = mcolorizer.Colorizer('3VarAddA', [mcolors.Normalize(),
                                           mcolors.Normalize(),
                                           'log'])
    cartist = mcolorizer.ColorizingArtist(ca)
    cartist.set_array(np.zeros((3, 5, 5)))
    with pytest.raises(ValueError, match='Complex numbers are incompatible with'):
        cartist.set_array(np.zeros((5, 5), dtype='complex128'))

