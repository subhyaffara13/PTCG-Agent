
def test_marker_rotated_invalid():
    marker = markers.MarkerStyle("o")
    with pytest.raises(ValueError):
        new_marker = marker.rotated()
    with pytest.raises(ValueError):
        new_marker = marker.rotated(deg=10, rad=10)

