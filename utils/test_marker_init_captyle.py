
def test_marker_init_captyle():
    marker = markers.MarkerStyle("*")
    styled_marker = markers.MarkerStyle("*", capstyle="round")
    assert styled_marker.get_capstyle() == "round"
    assert marker.get_capstyle() != "round"

