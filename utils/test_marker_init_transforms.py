
def test_marker_init_transforms():
    """Test that initializing marker with transform is a simple addition."""
    marker = markers.MarkerStyle("o")
    t = Affine2D().translate(1, 1)
    t_marker = markers.MarkerStyle("o", transform=t)
    assert marker.get_transform() + t == t_marker.get_transform()

