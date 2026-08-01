
def test_rectangle_selector_onselect(ax, interactive):
    # check when press and release events take place at the same position
    onselect = mock.Mock(spec=noop, return_value=None)

    tool = widgets.RectangleSelector(ax, onselect=onselect, interactive=interactive)
    # move outside of axis
    click_and_drag(tool, start=(100, 110), end=(150, 120))

    onselect.assert_called_once()
    assert tool.extents == (100.0, 150.0, 110.0, 120.0)

    onselect.reset_mock()
    click_and_drag(tool, start=(10, 100), end=(10, 100))
    onselect.assert_called_once()

