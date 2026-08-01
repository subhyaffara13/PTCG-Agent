
def test_marker_init_joinstyle():
    marker = markers.MarkerStyle("*")
    styled_marker = markers.MarkerStyle("*", joinstyle="round")
    assert styled_marker.get_joinstyle() == "round"
    assert marker.get_joinstyle() != "round"

