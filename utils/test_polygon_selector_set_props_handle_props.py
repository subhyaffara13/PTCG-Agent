
def test_polygon_selector_set_props_handle_props(ax, draw_bounding_box):
    tool = widgets.PolygonSelector(ax,
                                   props=dict(color='b', alpha=0.2),
                                   handle_props=dict(alpha=0.5),
                                   draw_bounding_box=draw_bounding_box)

    for event in [
        *polygon_place_vertex(ax, (50, 50)),
        *polygon_place_vertex(ax, (150, 50)),
        *polygon_place_vertex(ax, (50, 150)),
        *polygon_place_vertex(ax, (50, 50)),
    ]:
        event._process()

    artist = tool._selection_artist
    assert artist.get_color() == 'b'
    assert artist.get_alpha() == 0.2
    tool.set_props(color='r', alpha=0.3)
    assert artist.get_color() == 'r'
    assert artist.get_alpha() == 0.3

    for artist in tool._handles_artists:
        assert artist.get_color() == 'b'
        assert artist.get_alpha() == 0.5
    tool.set_handle_props(color='r', alpha=0.3)
    for artist in tool._handles_artists:
        assert artist.get_color() == 'r'
        assert artist.get_alpha() == 0.3

