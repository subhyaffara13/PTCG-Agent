
def _test_interactive_impl():
    import importlib.util
    import io
    import json
    import sys

    import pytest

    import matplotlib as mpl
    from matplotlib import pyplot as plt
    from matplotlib.backend_bases import KeyEvent, FigureCanvasBase
    mpl.rcParams.update({
        "webagg.open_in_browser": False,
    })

    mpl.rcParams.update(json.loads(sys.argv[1]))
    backend = plt.rcParams["backend"].lower()

    if backend.endswith("agg") and not backend.startswith(("gtk", "web")):
        # Force interactive framework setup.
        fig = plt.figure()
        plt.close(fig)

        # Check that we cannot switch to a backend using another interactive
        # framework, but can switch to a backend using cairo instead of agg,
        # or a non-interactive backend.  In the first case, we use tkagg as
        # the "other" interactive backend as it is (essentially) guaranteed
        # to be present.  Moreover, don't test switching away from gtk3 (as
        # Gtk.main_level() is not set up at this point yet) and webagg (which
        # uses no interactive framework).

        if backend != "tkagg":
            with pytest.raises(ImportError):
                mpl.use("tkagg", force=True)

        def check_alt_backend(alt_backend):
            mpl.use(alt_backend, force=True)
            fig = plt.figure()
            assert (type(fig.canvas).__module__ ==
                    f"matplotlib.backends.backend_{alt_backend}")
            plt.close("all")

        if importlib.util.find_spec("cairocffi"):
            check_alt_backend(backend[:-3] + "cairo")
        check_alt_backend("svg")
    mpl.use(backend, force=True)

    fig, ax = plt.subplots()
    assert type(fig.canvas).__module__ == f"matplotlib.backends.backend_{backend}"

    assert fig.canvas.manager.get_window_title() == "Figure 1"

    if mpl.rcParams["toolbar"] == "toolmanager":
        # test toolbar button icon LA mode see GH issue 25174
        _test_toolbar_button_la_mode_icon(fig)

    ax.plot([0, 1], [2, 3])
    if fig.canvas.toolbar:  # i.e toolbar2.
        fig.canvas.toolbar.draw_rubberband(None, 1., 1, 2., 2)

    if backend == 'webagg' and sys.version_info >= (3, 14):
        import asyncio
        asyncio.set_event_loop(asyncio.new_event_loop())

    timer = fig.canvas.new_timer(1.)  # Test that floats are cast to int.
    timer.add_callback(KeyEvent("key_press_event", fig.canvas, "q")._process)
    # Trigger quitting upon draw.
    fig.canvas.mpl_connect("draw_event", lambda event: timer.start())
    fig.canvas.mpl_connect("close_event", print)

    result = io.BytesIO()
    fig.savefig(result, format='png', dpi=100)

    plt.show()

    # Ensure that the window is really closed.
    plt.pause(0.5)

    # When the figure is closed, its manager is removed and the canvas is reset to
    # FigureCanvasBase. Saving should still be possible.
    assert type(fig.canvas) == FigureCanvasBase, str(fig.canvas)
    result_after = io.BytesIO()
    fig.savefig(result_after, format='png', dpi=100)

    if backend.endswith("agg"):
        # agg-based interactive backends should save the same image as a non-interactive
        # figure
        assert result.getvalue() == result_after.getvalue()

