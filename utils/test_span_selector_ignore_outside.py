
def test_span_selector_ignore_outside(ax, ignore_event_outside):
    onselect = mock.Mock(spec=noop, return_value=None)
    onmove = mock.Mock(spec=noop, return_value=None)

    tool = widgets.SpanSelector(ax, onselect, 'horizontal',
                                onmove_callback=onmove,
                                ignore_event_outside=ignore_event_outside)
    click_and_drag(tool, start=(100, 100), end=(125, 125))
    onselect.assert_called_once()
    onmove.assert_called_once()
    assert tool.extents == (100, 125)

    onselect.reset_mock()
    onmove.reset_mock()
    # Trigger event outside of span
    click_and_drag(tool, start=(150, 150), end=(160, 160))
    if ignore_event_outside:
        # event have been ignored and span haven't changed.
        onselect.assert_not_called()
        onmove.assert_not_called()
        assert tool.extents == (100, 125)
    else:
        # A new shape is created
        onselect.assert_called_once()
        onmove.assert_called_once()
        assert tool.extents == (150, 160)

