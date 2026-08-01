
def test_cm_set_cmap_error():
    sm = cm.ScalarMappable()
    # Pick a name we are pretty sure will never be a colormap name
    bad_cmap = 'AardvarksAreAwkward'
    with pytest.raises(ValueError, match=bad_cmap):
        sm.set_cmap(bad_cmap)

