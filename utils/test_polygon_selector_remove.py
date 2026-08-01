
def test_polygon_selector_remove(ax, idx, draw_bounding_box):
    verts = [(50, 50), (150, 50), (50, 150)]
    event_sequence = [polygon_place_vertex(ax, verts[0]),
                      polygon_place_vertex(ax, verts[1]),
                      polygon_place_vertex(ax, verts[2]),
                      # Finish the polygon
                      polygon_place_vertex(ax, verts[0])]
    # Add an extra point
    event_sequence.insert(idx, polygon_place_vertex(ax, (200, 200)))
    # Remove the extra point
    event_sequence.append(polygon_remove_vertex(ax, (200, 200)))
    # Flatten list of lists
    event_sequence = functools.reduce(operator.iadd, event_sequence, [])
    check_polygon_selector(event_sequence, verts, 2,
                           draw_bounding_box=draw_bounding_box)

