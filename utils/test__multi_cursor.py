
def test_MultiCursor(horizOn, vertOn, with_deprecated_canvas):
    fig = plt.figure()
    (ax1, ax3) = fig.subplots(2, sharex=True)
    ax2 = plt.figure().subplots()

    if with_deprecated_canvas:
        with pytest.warns(mpl.MatplotlibDeprecationWarning, match=r"canvas.*deprecat"):
            multi = widgets.MultiCursor(
                None, (ax1, ax2), useblit=False, horizOn=horizOn, vertOn=vertOn
            )
    else:
        # useblit=false to avoid having to draw the figure to cache the renderer
        multi = widgets.MultiCursor(
            (ax1, ax2), useblit=False, horizOn=horizOn, vertOn=vertOn
        )

    # Only two of the axes should have a line drawn on them.
    assert len(multi.vlines) == 2
    assert len(multi.hlines) == 2

    MouseEvent._from_ax_coords("motion_notify_event", ax1, (.5, .25))._process()
    # force a draw + draw event to exercise clear
    fig.canvas.draw()

    # the lines in the first two ax should both move
    for l in multi.vlines:
        assert l.get_xdata() == (.5, .5)
    for l in multi.hlines:
        assert l.get_ydata() == (.25, .25)
    # The relevant lines get turned on after move.
    assert len([line for line in multi.vlines if line.get_visible()]) == (
        2 if vertOn else 0)
    assert len([line for line in multi.hlines if line.get_visible()]) == (
        2 if horizOn else 0)

    # After toggling settings, the opposite lines should be visible after move.
    multi.horizOn = not multi.horizOn
    multi.vertOn = not multi.vertOn
    MouseEvent._from_ax_coords("motion_notify_event", ax1, (.5, .25))._process()
    assert len([line for line in multi.vlines if line.get_visible()]) == (
        0 if vertOn else 2)
    assert len([line for line in multi.hlines if line.get_visible()]) == (
        0 if horizOn else 2)

    # test a move event in an Axes not part of the MultiCursor
    # the lines in ax1 and ax2 should not have moved.
    MouseEvent._from_ax_coords("motion_notify_event", ax3, (.75, .75))._process()
    for l in multi.vlines:
        assert l.get_xdata() == (.5, .5)
    for l in multi.hlines:
        assert l.get_ydata() == (.25, .25)

