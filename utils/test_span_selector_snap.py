
def test_span_selector_snap(ax):
    def onselect(vmin, vmax):
        ax._got_onselect = True

    snap_values = np.arange(50) * 4

    tool = widgets.SpanSelector(ax, onselect, direction='horizontal',
                                snap_values=snap_values)
    tool.extents = (17, 35)
    assert tool.extents == (16, 36)

    tool.snap_values = None
    assert tool.snap_values is None
    tool.extents = (17, 35)
    assert tool.extents == (17, 35)

