
def assert_last_legend_patch_color(histogram, leg, expected_color,
                                   facecolor=False, edgecolor=False):
    """
    Check that histogram color, legend handle color, and legend label color all
    match the expected input. Provide facecolor and edgecolor flags to clarify
    which feature to match.
    """
    label_color = leg.texts[-1].get_color()
    patch = leg.get_patches()[-1]
    histogram = histogram[-1][0]
    assert mpl.colors.same_color(label_color, expected_color)
    if facecolor:
        assert mpl.colors.same_color(label_color, patch.get_facecolor())
        assert mpl.colors.same_color(label_color, histogram.get_facecolor())
    if edgecolor:
        assert mpl.colors.same_color(label_color, patch.get_edgecolor())
        assert mpl.colors.same_color(label_color, histogram.get_edgecolor())

