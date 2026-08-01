
def test_span_selector_onselect(ax, interactive):
    onselect = mock.Mock(spec=noop, return_value=None)

    tool = widgets.SpanSelector(ax, onselect, 'horizontal',
                                interactive=interactive)
    # move outside of axis
    click_and_drag(tool, start=(100, 100), end=(150, 100))
    onselect.assert_called_once()
    assert tool.extents == (100, 150)

    onselect.reset_mock()
    click_and_drag(tool, start=(10, 100), end=(10, 100))
    onselect.assert_called_once()

