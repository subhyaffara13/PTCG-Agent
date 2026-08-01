
def check_polygon_selector(events, expected, selections_count, **kwargs):
    """
    Helper function to test Polygon Selector.

    Parameters
    ----------
    events : list[MouseEvent]
        A sequence of events to perform.
    expected : list of vertices (xdata, ydata)
        The list of vertices expected to result from the event sequence.
    selections_count : int
        Wait for the tool to call its `onselect` function `selections_count`
        times, before comparing the result to the `expected`
    **kwargs
        Keyword arguments are passed to PolygonSelector.
    """
    onselect = mock.Mock(spec=noop, return_value=None)

    ax = events[0].canvas.figure.axes[0]
    tool = widgets.PolygonSelector(ax, onselect=onselect, **kwargs)

    for event in events:
        event._process()

    assert onselect.call_count == selections_count
    assert onselect.call_args == ((expected, ), {})

