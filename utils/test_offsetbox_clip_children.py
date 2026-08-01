
def test_offsetbox_clip_children():
    # - create a plot
    # - put an AnchoredOffsetbox with a child DrawingArea
    #   at the center of the axes
    # - give the DrawingArea a gray background
    # - put a black line across the bounds of the DrawingArea
    # - see that the black line is clipped to the edges of
    #   the DrawingArea.
    fig, ax = plt.subplots()
    size = 100
    da = DrawingArea(size, size, clip=True)
    bg = mpatches.Rectangle((0, 0), size, size,
                            facecolor='#CCCCCC',
                            edgecolor='None',
                            linewidth=0)
    line = mlines.Line2D([-size*.5, size*1.5], [size/2, size/2],
                         color='black',
                         linewidth=10)
    anchored_box = AnchoredOffsetbox(
        loc='center',
        child=da,
        pad=0.,
        frameon=False,
        bbox_to_anchor=(.5, .5),
        bbox_transform=ax.transAxes,
        borderpad=0.)

    da.add_artist(bg)
    da.add_artist(line)
    ax.add_artist(anchored_box)

    fig.canvas.draw()
    assert not fig.stale
    da.clip_children = True
    assert fig.stale

