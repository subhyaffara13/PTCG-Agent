
def test_span_selector_set_props_handle_props(ax):
    tool = widgets.SpanSelector(ax, onselect=noop, direction='horizontal',
                                interactive=True,
                                props=dict(facecolor='b', alpha=0.2),
                                handle_props=dict(alpha=0.5))
    # Create rectangle
    click_and_drag(tool, start=(0, 10), end=(100, 120))

    artist = tool._selection_artist
    assert artist.get_facecolor() == mcolors.to_rgba('b', alpha=0.2)
    tool.set_props(facecolor='r', alpha=0.3)
    assert artist.get_facecolor() == mcolors.to_rgba('r', alpha=0.3)

    for artist in tool._handles_artists:
        assert artist.get_color() == 'b'
        assert artist.get_alpha() == 0.5
    tool.set_handle_props(color='r', alpha=0.3)
    for artist in tool._handles_artists:
        assert artist.get_color() == 'r'
        assert artist.get_alpha() == 0.3

