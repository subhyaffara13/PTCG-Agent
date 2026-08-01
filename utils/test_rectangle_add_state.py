
def test_rectangle_add_state(ax):
    tool = widgets.RectangleSelector(ax, interactive=True)
    # Create rectangle
    click_and_drag(tool, start=(70, 65), end=(125, 130))

    with pytest.raises(ValueError):
        tool.add_state('unsupported_state')

    with pytest.raises(ValueError):
        tool.add_state('clear')
    tool.add_state('move')
    tool.add_state('square')
    tool.add_state('center')

