
def test_markers_invalid(marker):
    with pytest.raises(ValueError):
        markers.MarkerStyle(marker)

