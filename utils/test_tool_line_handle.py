
def test_tool_line_handle(ax):
    positions = [20, 30, 50]
    tool_line_handle = widgets.ToolLineHandles(ax, positions, 'horizontal',
                                               useblit=False)

    for artist in tool_line_handle.artists:
        assert not artist.get_animated()
        assert not artist.get_visible()

    tool_line_handle.set_visible(True)
    tool_line_handle.set_animated(True)

    for artist in tool_line_handle.artists:
        assert artist.get_animated()
        assert artist.get_visible()

    assert tool_line_handle.positions == positions

