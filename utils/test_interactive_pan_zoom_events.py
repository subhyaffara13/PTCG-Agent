
def test_interactive_pan_zoom_events(tool, button, patch_vis, forward_nav, t_s):
    # Bottom axes: ax_b    Top axes: ax_t
    fig, ax_b = plt.subplots()
    ax_t = fig.add_subplot(221, zorder=99)
    ax_t.set_forward_navigation_events(forward_nav)
    ax_t.patch.set_visible(patch_vis)

    # ----------------------------
    if t_s == "share":
        ax_t_twin = fig.add_subplot(222)
        ax_t_twin.sharex(ax_t)
        ax_t_twin.sharey(ax_t)

        ax_b_twin = fig.add_subplot(223)
        ax_b_twin.sharex(ax_b)
        ax_b_twin.sharey(ax_b)
    elif t_s == "twin":
        ax_t_twin = ax_t.twinx()
        ax_b_twin = ax_b.twinx()

    # just some styling to simplify manual checks
    ax_t.set_label("ax_t")
    ax_t.patch.set_facecolor((1, 0, 0, 0.5))

    ax_t_twin.set_label("ax_t_twin")
    ax_t_twin.patch.set_facecolor("r")

    ax_b.set_label("ax_b")
    ax_b.patch.set_facecolor((0, 0, 1, 0.5))

    ax_b_twin.set_label("ax_b_twin")
    ax_b_twin.patch.set_facecolor("b")

    # ----------------------------

    # Set initial axis limits
    init_xlim, init_ylim = (0, 10), (0, 10)
    for ax in [ax_t, ax_b]:
        ax.set_xlim(*init_xlim)
        ax.set_ylim(*init_ylim)

    # Mouse from 2 to 1 (in data-coordinates of ax_t).
    xstart_t, xstop_t, ystart_t, ystop_t = 1, 2, 1, 2
    # Convert to screen coordinates ("s").  Events are defined only with pixel
    # precision, so round the pixel values, and below, check against the
    # corresponding xdata/ydata, which are close but not equal to s0/s1.
    s0 = ax_t.transData.transform((xstart_t, ystart_t)).astype(int)
    s1 = ax_t.transData.transform((xstop_t, ystop_t)).astype(int)

    # Calculate the mouse-distance in data-coordinates of the bottom-axes
    xstart_b, ystart_b = ax_b.transData.inverted().transform(s0)
    xstop_b, ystop_b = ax_b.transData.inverted().transform(s1)

    # Set up the mouse movements
    start_event = MouseEvent("button_press_event", fig.canvas, *s0, button)
    drag_event = MouseEvent(
        "motion_notify_event", fig.canvas, *s1, button, buttons={button})
    stop_event = MouseEvent("button_release_event", fig.canvas, *s1, button)

    tb = NavigationToolbar2(fig.canvas)

    if tool == "zoom":
        # Evaluate expected limits before executing the zoom-event
        direction = ("in" if button == 1 else "out")

        xlim_t, ylim_t = ax_t._prepare_view_from_bbox([*s0, *s1], direction)

        if ax_t.get_forward_navigation_events() is True:
            xlim_b, ylim_b = ax_b._prepare_view_from_bbox([*s0, *s1], direction)
        elif ax_t.get_forward_navigation_events() is False:
            xlim_b = init_xlim
            ylim_b = init_ylim
        else:
            if not ax_t.patch.get_visible():
                xlim_b, ylim_b = ax_b._prepare_view_from_bbox([*s0, *s1], direction)
            else:
                xlim_b = init_xlim
                ylim_b = init_ylim

        tb.zoom()

    else:
        # Evaluate expected limits
        # (call start_pan to make sure ax._pan_start is set)
        ax_t.start_pan(*s0, button)
        xlim_t, ylim_t = ax_t._get_pan_points(button, None, *s1).T.astype(float)
        ax_t.end_pan()

        if ax_t.get_forward_navigation_events() is True:
            ax_b.start_pan(*s0, button)
            xlim_b, ylim_b = ax_b._get_pan_points(button, None, *s1).T.astype(float)
            ax_b.end_pan()
        elif ax_t.get_forward_navigation_events() is False:
            xlim_b = init_xlim
            ylim_b = init_ylim
        else:
            if not ax_t.patch.get_visible():
                ax_b.start_pan(*s0, button)
                xlim_b, ylim_b = ax_b._get_pan_points(button, None, *s1).T.astype(float)
                ax_b.end_pan()
            else:
                xlim_b = init_xlim
                ylim_b = init_ylim

        tb.pan()

    start_event._process()
    drag_event._process()
    stop_event._process()

    assert ax_t.get_xlim() == pytest.approx(xlim_t, abs=0.15)
    assert ax_t.get_ylim() == pytest.approx(ylim_t, abs=0.15)
    assert ax_b.get_xlim() == pytest.approx(xlim_b, abs=0.15)
    assert ax_b.get_ylim() == pytest.approx(ylim_b, abs=0.15)

    # Check if twin-axes are properly triggered
    assert ax_t.get_xlim() == pytest.approx(ax_t_twin.get_xlim(), abs=0.15)
    assert ax_b.get_xlim() == pytest.approx(ax_b_twin.get_xlim(), abs=0.15)

