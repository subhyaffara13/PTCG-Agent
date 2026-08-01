
def test_span_selector_drag(ax, drag_from_anywhere):
    # Create span
    tool = widgets.SpanSelector(ax, onselect=noop, direction='horizontal',
                                interactive=True,
                                drag_from_anywhere=drag_from_anywhere)
    click_and_drag(tool, start=(10, 10), end=(100, 120))
    assert tool.extents == (10, 100)
    # Drag inside span
    #
    # If drag_from_anywhere == True, this will move the span by 10,
    # giving new value extents = 20, 110
    #
    # If drag_from_anywhere == False, this will create a new span with
    # value extents = 25, 35
    click_and_drag(tool, start=(25, 15), end=(35, 25))
    if drag_from_anywhere:
        assert tool.extents == (20, 110)
    else:
        assert tool.extents == (25, 35)

    # Check that in both cases, dragging outside the span draws a new span
    click_and_drag(tool, start=(175, 185), end=(185, 195))
    assert tool.extents == (175, 185)

