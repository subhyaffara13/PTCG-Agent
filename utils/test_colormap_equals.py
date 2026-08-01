
def test_colormap_equals():
    cmap = mpl.colormaps["plasma"]
    cm_copy = cmap.copy()
    # different object id's
    assert cm_copy is not cmap
    # But the same data should be equal
    assert cm_copy == cmap
    # Change the copy
    with pytest.warns(PendingDeprecationWarning):
        cm_copy.set_bad('y')
    assert cm_copy != cmap
    # Make sure we can compare different sizes without failure
    cm_copy._lut = cm_copy._lut[:10, :]
    assert cm_copy != cmap
    # Test different names are equal if the lookup table is the same
    cm_copy = cmap.copy()
    cm_copy.name = "Test"
    assert cm_copy == cmap
    # Test colorbar extends
    cm_copy = cmap.copy()
    cm_copy.colorbar_extend = not cmap.colorbar_extend
    assert cm_copy != cmap

