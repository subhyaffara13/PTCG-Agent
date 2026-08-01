
def test_polygon_selector_box(ax):
    # Create a diamond (adjusting axes lims s.t. the diamond lies within axes limits).
    ax.set(xlim=(-10, 50), ylim=(-10, 50))
    verts = [(20, 0), (0, 20), (20, 40), (40, 20)]
    event_sequence = [
        *polygon_place_vertex(ax, verts[0]),
        *polygon_place_vertex(ax, verts[1]),
        *polygon_place_vertex(ax, verts[2]),
        *polygon_place_vertex(ax, verts[3]),
        *polygon_place_vertex(ax, verts[0]),
    ]

    # Create selector
    tool = widgets.PolygonSelector(ax, draw_bounding_box=True)
    for event in event_sequence:
        event._process()

    # Scale to half size using the top right corner of the bounding box
    MouseEvent._from_ax_coords("button_press_event", ax, (40, 40), 1)._process()
    MouseEvent._from_ax_coords("motion_notify_event", ax, (20, 20))._process()
    MouseEvent._from_ax_coords("button_release_event", ax, (20, 20), 1)._process()
    np.testing.assert_allclose(
        tool.verts, [(10, 0), (0, 10), (10, 20), (20, 10)])

    # Move using the center of the bounding box
    MouseEvent._from_ax_coords("button_press_event", ax, (10, 10), 1)._process()
    MouseEvent._from_ax_coords("motion_notify_event", ax, (30, 30))._process()
    MouseEvent._from_ax_coords("button_release_event", ax, (30, 30), 1)._process()
    np.testing.assert_allclose(
        tool.verts, [(30, 20), (20, 30), (30, 40), (40, 30)])

    # Remove a point from the polygon and check that the box extents update
    np.testing.assert_allclose(
        tool._box.extents, (20.0, 40.0, 20.0, 40.0))

    MouseEvent._from_ax_coords("button_press_event", ax, (30, 20), 3)._process()
    MouseEvent._from_ax_coords("button_release_event", ax, (30, 20), 3)._process()
    np.testing.assert_allclose(
        tool.verts, [(20, 30), (30, 40), (40, 30)])
    np.testing.assert_allclose(
        tool._box.extents, (20.0, 40.0, 30.0, 40.0))

