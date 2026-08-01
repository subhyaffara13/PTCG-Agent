
def test_polygon_selector_box_props_handle_props(ax):
    props = dict(color='r')
    handle_props = dict(marker='o', markerfacecolor='w', markeredgecolor='r')
    box_props = dict(linestyle=':', facecolor='c', edgecolor='b')
    box_handle_props = dict(markeredgecolor='y')

    tool = widgets.PolygonSelector(
        ax, draw_bounding_box=True,
        props=props, handle_props=handle_props,
        box_props=box_props, box_handle_props=box_handle_props)

    for event in [
        *polygon_place_vertex(ax, (50, 50)),
        *polygon_place_vertex(ax, (150, 50)),
        *polygon_place_vertex(ax, (50, 150)),
        *polygon_place_vertex(ax, (50, 50)),
    ]:
        event._process()

    artist = tool._selection_artist
    assert mcolors.same_color(artist.get_color(), 'r')
    for artist in tool._handles_artists:
        assert artist.get_marker() == 'o'
        assert mcolors.same_color(artist.get_markerfacecolor(), 'w')
        assert mcolors.same_color(artist.get_markeredgecolor(), 'r')

    box_artist = tool._box._selection_artist
    assert box_artist.get_linestyle() == ':'
    assert mcolors.same_color(box_artist.get_facecolor(), 'c')
    assert mcolors.same_color(box_artist.get_edgecolor(), 'b')
    for artist in tool._box._handles_artists:
        # marker and markerfacecolor are inherited from handle_props
        # markeredgecolor is overridden by box_handle_props.
        assert artist.get_marker() == 'o'
        assert mcolors.same_color(artist.get_markerfacecolor(), 'w')
        assert mcolors.same_color(artist.get_markeredgecolor(), 'y')

