
def test_bivar_resample():
    cmap = mpl.bivar_colormaps['BiOrangeBlue']

    assert_allclose(cmap.resampled((2, 2))((0.25, 0.25)), (0, 0, 0, 1))
    assert_allclose(cmap.resampled((-2, 2))((0.25, 0.25)), (1., 0.5, 0., 1.))
    assert_allclose(cmap.resampled((2, -2))((0.25, 0.25)), (0., 0.5, 1., 1.))
    assert_allclose(cmap.resampled((-2, -2))((0.25, 0.25)), (1, 1, 1, 1))

    assert_allclose(cmap((0.8, 0.4)), (0.8, 0.6, 0.4, 1.))
    assert_allclose(cmap.reversed()((1 - 0.8, 1 - 0.4)), (0.8, 0.6, 0.4, 1.))

    assert_allclose(cmap((0.6, 0.2)), (0.6, 0.4, 0.2, 1.))
    assert_allclose(cmap.transposed()((0.2, 0.6)), (0.6, 0.4, 0.2, 1.))

    with pytest.raises(ValueError, match="lutshape must be of length"):
        cmap = cmap.resampled(4)

