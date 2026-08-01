
def test_rectangle_selector_ignore_outside(ax, ignore_event_outside):
    onselect = mock.Mock(spec=noop, return_value=None)

    tool = widgets.RectangleSelector(ax, onselect=onselect,
                                     ignore_event_outside=ignore_event_outside)
    click_and_drag(tool, start=(100, 110), end=(150, 120))
    onselect.assert_called_once()
    assert tool.extents == (100.0, 150.0, 110.0, 120.0)

    onselect.reset_mock()
    # Trigger event outside of span
    click_and_drag(tool, start=(150, 150), end=(160, 160))
    if ignore_event_outside:
        # event have been ignored and span haven't changed.
        onselect.assert_not_called()
        assert tool.extents == (100.0, 150.0, 110.0, 120.0)
    else:
        # A new shape is created
        onselect.assert_called_once()
        assert tool.extents == (150.0, 160.0, 150.0, 160.0)

