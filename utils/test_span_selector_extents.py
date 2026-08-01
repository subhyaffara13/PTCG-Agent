
def test_span_selector_extents(ax):
    tool = widgets.SpanSelector(
        ax, lambda a, b: None, "horizontal", ignore_event_outside=True
        )
    tool.extents = (5, 10)

    assert tool.extents == (5, 10)
    assert tool._selection_completed

    # Since `ignore_event_outside=True`, this event should be ignored
    press_data = (12, 14)
    release_data = (20, 14)
    click_and_drag(tool, start=press_data, end=release_data)

    assert tool.extents == (5, 10)

