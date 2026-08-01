
def test_polygon_selector_verts_setter(fig_test, fig_ref, draw_bounding_box):
    verts = [(0.1, 0.4), (0.5, 0.9), (0.3, 0.2)]
    ax_test = fig_test.add_subplot()

    tool_test = widgets.PolygonSelector(ax_test, draw_bounding_box=draw_bounding_box)
    tool_test.verts = verts
    assert tool_test.verts == verts

    ax_ref = fig_ref.add_subplot()
    tool_ref = widgets.PolygonSelector(ax_ref, draw_bounding_box=draw_bounding_box)
    for event in [
        *polygon_place_vertex(ax_ref, verts[0]),
        *polygon_place_vertex(ax_ref, verts[1]),
        *polygon_place_vertex(ax_ref, verts[2]),
        *polygon_place_vertex(ax_ref, verts[0]),
    ]:
        event._process()

