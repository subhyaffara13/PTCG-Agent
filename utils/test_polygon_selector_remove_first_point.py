
def test_polygon_selector_remove_first_point(ax, draw_bounding_box):
    verts = [(50, 50), (150, 50), (50, 150)]
    event_sequence = [
        *polygon_place_vertex(ax, verts[0]),
        *polygon_place_vertex(ax, verts[1]),
        *polygon_place_vertex(ax, verts[2]),
        *polygon_place_vertex(ax, verts[0]),
        *polygon_remove_vertex(ax, verts[0]),
    ]
    check_polygon_selector(event_sequence, verts[1:], 2,
                           draw_bounding_box=draw_bounding_box)

