
def test_colorizer_bivar_cmap():
    ca = mcolorizer.Colorizer('BiOrangeBlue', [mcolors.Normalize(), 'log'])

    with pytest.raises(ValueError, match='The colormap viridis'):
        ca.cmap = 'viridis'

    cartist = mcolorizer.ColorizingArtist(ca)
    cartist.set_array(np.zeros((2, 4, 4)))

    with pytest.raises(ValueError, match='Invalid data entry for multivariate'):
        cartist.set_array(np.zeros((3, 4, 4)))

    dt = np.dtype([('x', 'f4'), ('', 'object')])
    with pytest.raises(TypeError, match='converted to a sequence of floats'):
        cartist.set_array(np.zeros((2, 4, 4), dtype=dt))

    with pytest.raises(ValueError, match='all variates must have same shape'):
        cartist.set_array((np.zeros(3), np.zeros(4)))

    # ensure masked value is propagated from input
    a = np.arange(3)
    cartist.set_array((a, np.ma.masked_where(a > 1, a)))
    assert np.all(cartist.get_array()['f0'].mask == np.array([0, 0, 0], dtype=bool))
    assert np.all(cartist.get_array()['f1'].mask == np.array([0, 0, 1], dtype=bool))

    # test clearing data
    cartist.set_array(None)
    cartist.get_array() is None

