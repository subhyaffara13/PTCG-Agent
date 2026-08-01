
def test_bivar_cmap_call_tuple():
    cmap = mpl.bivar_colormaps['BiOrangeBlue']
    assert_allclose(cmap((1.0, 1.0)), (1, 1, 1, 1))
    assert_allclose(cmap((0.0, 0.0)), (0, 0, 0, 1))
    assert_allclose(cmap((0.2, 0.8)), (0.2, 0.5, 0.8, 1))
    assert_allclose(cmap((0.0, 0.0), alpha=0.1), (0, 0, 0, 0.1))

