
def test_bivar_cmap_lut_smooth():
    cmap = mpl.bivar_colormaps['BiOrangeBlue']

    assert_allclose(cmap.lut[:, 0, 0], np.linspace(0, 1, 256))
    assert_allclose(cmap.lut[:, 255, 0], np.linspace(0, 1, 256))
    assert_allclose(cmap.lut[:, 0, 1], np.linspace(0, 0.5, 256))
    assert_allclose(cmap.lut[:, 153, 1], np.linspace(0.3, 0.8, 256))
    assert_allclose(cmap.lut[:, 255, 1], np.linspace(0.5, 1, 256))

    assert_allclose(cmap.lut[0, :, 1], np.linspace(0, 0.5, 256))
    assert_allclose(cmap.lut[102, :, 1], np.linspace(0.2, 0.7, 256))
    assert_allclose(cmap.lut[255, :, 1], np.linspace(0.5, 1, 256))
    assert_allclose(cmap.lut[0, :, 2], np.linspace(0, 1, 256))
    assert_allclose(cmap.lut[255, :, 2], np.linspace(0, 1, 256))

