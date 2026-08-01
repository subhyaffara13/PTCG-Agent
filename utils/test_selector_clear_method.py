
def test_selector_clear_method(ax, selector):
    if selector == 'span':
        tool = widgets.SpanSelector(ax, onselect=noop, direction='horizontal',
                                    interactive=True,
                                    ignore_event_outside=True)
    else:
        tool = widgets.RectangleSelector(ax, interactive=True)
    click_and_drag(tool, start=(10, 10), end=(100, 120))
    assert tool._selection_completed
    assert tool.get_visible()
    if selector == 'span':
        assert tool.extents == (10, 100)

    tool.clear()
    assert not tool._selection_completed
    assert not tool.get_visible()

    # Do another cycle of events to make sure we can
    click_and_drag(tool, start=(10, 10), end=(50, 120))
    assert tool._selection_completed
    assert tool.get_visible()
    if selector == 'span':
        assert tool.extents == (10, 50)

