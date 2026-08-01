
def test_bivar_cmap_1d_origin():
    """
    Test getting 1D colormaps with different origins
    """
    cmap0 = mpl.bivar_colormaps['BiOrangeBlue']
    assert_allclose(cmap0[0].colors[:, 0], np.linspace(0, 1, 256))
    assert_allclose(cmap0[0].colors[:, 1], np.linspace(0, 0.5, 256))
    assert_allclose(cmap0[0].colors[:, 2], 0)
    assert_allclose(cmap0[1].colors[:, 0], 0)
    assert_allclose(cmap0[1].colors[:, 1], np.linspace(0, 0.5, 256))
    assert_allclose(cmap0[1].colors[:, 2], np.linspace(0, 1, 256))

    cmap1 = cmap0.with_extremes(origin=(0, 1))
    assert_allclose(cmap1[0].colors[:, 0], np.linspace(0, 1, 256))
    assert_allclose(cmap1[0].colors[:, 1], np.linspace(0.5, 1, 256))
    assert_allclose(cmap1[0].colors[:, 2], 1)
    assert_allclose(cmap1[1].colors, cmap0[1].colors)

    cmap2 = cmap0.with_extremes(origin=(0.2, 0.4))
    assert_allclose(cmap2[0].colors[:, 0], np.linspace(0, 1, 256))
    assert_allclose(cmap2[0].colors[:, 1], np.linspace(0.2, 0.7, 256))
    assert_allclose(cmap2[0].colors[:, 2], 0.4)
    assert_allclose(cmap2[1].colors[:, 0], 0.2)
    assert_allclose(cmap2[1].colors[:, 1], np.linspace(0.1, 0.6, 256))
    assert_allclose(cmap2[1].colors[:, 2], np.linspace(0, 1, 256))

    with pytest.raises(KeyError,
                       match="only 0 or 1 are valid keys"):
        cs = cmap0[2]

