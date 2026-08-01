
def test_axis_artist():
    fig, ax = plt.subplots()

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    for loc in ('left', 'right', 'bottom'):
        helper = AxisArtistHelperRectlinear.Fixed(ax, loc=loc)
        axisline = AxisArtist(ax, helper, offset=None, axis_direction=loc)
        axisline.major_ticks.set_tick_direction({
            "left": "in", "right": "out", "bottom": "inout",
        }[loc])
        ax.add_artist(axisline)

    # Settings for bottom AxisArtist.
    axisline.set_label("TTT")
    axisline.label.set_pad(5)

    ax.set_ylabel("Test")

