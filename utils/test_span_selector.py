
def test_span_selector(ax, orientation, onmove_callback, kwargs):
    # Also test that span selectors work in the presence of twin axes or for
    # outside-inset axes on top of the axes that contain the selector.  Note
    # that we need to unforce the axes aspect here, otherwise the twin axes
    # forces the original axes' limits (to respect aspect=1) which makes some
    # of the values below go out of bounds.
    ax.set_aspect("auto")
    ax.twinx()
    child = ax.inset_axes([0, 1, 1, 1], xlim=(0, 200), ylim=(0, 200))

    for target in [ax, child]:
        selected = []
        def onselect(*args): selected.append(args)
        moved = []
        def onmove(*args): moved.append(args)
        if onmove_callback:
            kwargs['onmove_callback'] = onmove

        tool = widgets.SpanSelector(target, onselect, orientation, **kwargs)
        MouseEvent._from_ax_coords(
            "button_press_event", target, (100, 100), 1)._process()
        # move outside of axis
        MouseEvent._from_ax_coords(
            "motion_notify_event", target, (199, 199), 1)._process()
        MouseEvent._from_ax_coords(
            "button_release_event", target, (250, 250), 1)._process()

        # tol is set by pixel size (~100 pixels & span of 200 data units)
        assert_allclose(selected, [(100, 199)], atol=.5)
        if onmove_callback:
            assert_allclose(moved, [(100, 199)], atol=.5)

