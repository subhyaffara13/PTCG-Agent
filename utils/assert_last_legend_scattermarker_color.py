
def assert_last_legend_scattermarker_color(scatter_marker, leg, expected_color,
                                           facecolor=False, edgecolor=False):
    """
    Check that scatter marker color, legend handle color, and legend label color all
    match the expected input. Provide facecolor and edgecolor flags to clarify
    which feature to match.
    """
    label_color = leg.texts[-1].get_color()
    leg_handle = leg.legend_handles[-1]
    assert mpl.colors.same_color(label_color, expected_color)
    if facecolor:
        assert mpl.colors.same_color(label_color, leg_handle.get_facecolor())
        assert mpl.colors.same_color(label_color, scatter_marker.get_facecolor())
    if edgecolor:
        assert mpl.colors.same_color(label_color, leg_handle.get_edgecolor())
        assert mpl.colors.same_color(label_color, scatter_marker.get_edgecolor())

