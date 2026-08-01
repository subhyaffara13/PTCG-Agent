
def test_polygon_selector_redraw(ax, draw_bounding_box):
    verts = [(50, 50), (150, 50), (50, 150)]
    event_sequence = [
        *polygon_place_vertex(ax, verts[0]),
        *polygon_place_vertex(ax, verts[1]),
        *polygon_place_vertex(ax, verts[2]),
        *polygon_place_vertex(ax, verts[0]),
        # Polygon completed, now remove first two verts.
        *polygon_remove_vertex(ax, verts[1]),
        *polygon_remove_vertex(ax, verts[2]),
        # At this point the tool should be reset so we can add more vertices.
        *polygon_place_vertex(ax, verts[1]),
    ]

    tool = widgets.PolygonSelector(ax, draw_bounding_box=draw_bounding_box)
    for event in event_sequence:
        event._process()
    # After removing two verts, only one remains, and the
    # selector should be automatically reset
    assert tool.verts == verts[0:2]

