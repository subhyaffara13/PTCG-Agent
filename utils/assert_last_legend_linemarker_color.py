
def assert_last_legend_linemarker_color(line_marker, leg, expected_color, color=False,
                                        facecolor=False, edgecolor=False):
    """
    Check that line marker color, legend handle color, and legend label color all
    match the expected input. Provide color, facecolor and edgecolor flags to clarify
    which feature to match.
    """
    label_color = leg.texts[-1].get_color()
    leg_marker = leg.get_lines()[-1]
    assert mpl.colors.same_color(label_color, expected_color)
    if color:
        assert mpl.colors.same_color(label_color, leg_marker.get_color())
        assert mpl.colors.same_color(label_color, line_marker.get_color())
    if facecolor:
        assert mpl.colors.same_color(label_color, leg_marker.get_markerfacecolor())
        assert mpl.colors.same_color(label_color, line_marker.get_markerfacecolor())
    if edgecolor:
        assert mpl.colors.same_color(label_color, leg_marker.get_markeredgecolor())
        assert mpl.colors.same_color(label_color, line_marker.get_markeredgecolor())

