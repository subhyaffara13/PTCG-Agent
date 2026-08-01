
def test_snapping_values_span_selector(ax):
    def onselect(*args):
        pass

    tool = widgets.SpanSelector(ax, onselect, direction='horizontal',)
    snap_function = tool._snap

    snap_values = np.linspace(0, 5, 11)
    values = np.array([-0.1, 0.1, 0.2, 0.5, 0.6, 0.7, 0.9, 4.76, 5.0, 5.5])
    expect = np.array([00.0, 0.0, 0.0, 0.5, 0.5, 0.5, 1.0, 5.00, 5.0, 5.0])
    values = snap_function(values, snap_values)
    assert_allclose(values, expect)

