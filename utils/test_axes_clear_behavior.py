
def test_axes_clear_behavior(fig_ref, fig_test, which):
    """Test that the given tick params are not reset by ax.clear()."""
    ax_test = fig_test.subplots()
    ax_ref = fig_ref.subplots()
    # the following tick params values are chosen to each create a visual difference
    # from their defaults
    target = {
        "direction": "in",
        "length": 10,
        "width": 10,
        "color": "xkcd:wine red",
        "pad": 0,
        "labelfontfamily": "serif",
        "zorder": 7,
        "labelrotation": 45,
        "labelcolor": "xkcd:shocking pink",
        # this overrides color + labelcolor, skip
        # colors: ,
        "grid_color": "xkcd:fluorescent green",
        "grid_alpha": 0.5,
        "grid_linewidth": 3,
        "grid_linestyle": ":",
        "bottom": False,
        "top": True,
        "left": False,
        "right": True,
        "labelbottom": True,
        "labeltop": True,
        "labelleft": True,
        "labelright": True,
    }

    ax_ref.tick_params(axis=which, **target)

    ax_test.tick_params(axis=which, **target)
    ax_test.clear()

    ax_ref.grid(True)
    ax_test.grid(True)

