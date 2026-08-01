
def test_polygon_selector(ax, draw_bounding_box):
    check_selector = functools.partial(
        check_polygon_selector, draw_bounding_box=draw_bounding_box)

    # Simple polygon
    expected_result = [(50, 50), (150, 50), (50, 150)]
    event_sequence = [
        *polygon_place_vertex(ax, (50, 50)),
        *polygon_place_vertex(ax, (150, 50)),
        *polygon_place_vertex(ax, (50, 150)),
        *polygon_place_vertex(ax, (50, 50)),
    ]
    check_selector(event_sequence, expected_result, 1)

    # Move first vertex before completing the polygon.
    expected_result = [(75, 50), (150, 50), (50, 150)]
    event_sequence = [
        *polygon_place_vertex(ax, (50, 50)),
        *polygon_place_vertex(ax, (150, 50)),
        KeyEvent("key_press_event", ax.figure.canvas, "control"),
        MouseEvent._from_ax_coords("motion_notify_event", ax, (50, 50)),
        MouseEvent._from_ax_coords("button_press_event", ax, (50, 50), 1),
        MouseEvent._from_ax_coords("motion_notify_event", ax, (75, 50)),
        MouseEvent._from_ax_coords("button_release_event", ax, (75, 50), 1),
        KeyEvent("key_release_event", ax.figure.canvas, "control"),
        *polygon_place_vertex(ax, (50, 150)),
        *polygon_place_vertex(ax, (75, 50)),
    ]
    check_selector(event_sequence, expected_result, 1)

    # Move first two vertices at once before completing the polygon.
    expected_result = [(50, 75), (150, 75), (50, 150)]
    event_sequence = [
        *polygon_place_vertex(ax, (50, 50)),
        *polygon_place_vertex(ax, (150, 50)),
        KeyEvent("key_press_event", ax.figure.canvas, "shift"),
        MouseEvent._from_ax_coords("motion_notify_event", ax, (100, 100)),
        MouseEvent._from_ax_coords("button_press_event", ax, (100, 100), 1),
        MouseEvent._from_ax_coords("motion_notify_event", ax, (100, 125)),
        MouseEvent._from_ax_coords("button_release_event", ax, (100, 125), 1),
        KeyEvent("key_release_event", ax.figure.canvas, "shift"),
        *polygon_place_vertex(ax, (50, 150)),
        *polygon_place_vertex(ax, (50, 75)),
    ]
    check_selector(event_sequence, expected_result, 1)

    # Move first vertex after completing the polygon.
    expected_result = [(85, 50), (150, 50), (50, 150)]
    event_sequence = [
        *polygon_place_vertex(ax, (60, 50)),
        *polygon_place_vertex(ax, (150, 50)),
        *polygon_place_vertex(ax, (50, 150)),
        *polygon_place_vertex(ax, (60, 50)),
        MouseEvent._from_ax_coords("motion_notify_event", ax, (60, 50)),
        MouseEvent._from_ax_coords("button_press_event", ax, (60, 50), 1),
        MouseEvent._from_ax_coords("motion_notify_event", ax, (85, 50)),
        MouseEvent._from_ax_coords("button_release_event", ax, (85, 50), 1),
    ]
    check_selector(event_sequence, expected_result, 2)

    # Move all vertices after completing the polygon.
    expected_result = [(75, 75), (175, 75), (75, 175)]
    event_sequence = [
        *polygon_place_vertex(ax, (50, 50)),
        *polygon_place_vertex(ax, (150, 50)),
        *polygon_place_vertex(ax, (50, 150)),
        *polygon_place_vertex(ax, (50, 50)),
        KeyEvent("key_press_event", ax.figure.canvas, "shift"),
        MouseEvent._from_ax_coords("motion_notify_event", ax, (100, 100)),
        MouseEvent._from_ax_coords("button_press_event", ax, (100, 100), 1),
        MouseEvent._from_ax_coords("motion_notify_event", ax, (125, 125)),
        MouseEvent._from_ax_coords("button_release_event", ax, (125, 125), 1),
        KeyEvent("key_release_event", ax.figure.canvas, "shift"),
    ]
    check_selector(event_sequence, expected_result, 2)

    # Try to move a vertex and move all before placing any vertices.
    expected_result = [(50, 50), (150, 50), (50, 150)]
    event_sequence = [
        KeyEvent("key_press_event", ax.figure.canvas, "control"),
        MouseEvent._from_ax_coords("motion_notify_event", ax, (100, 100)),
        MouseEvent._from_ax_coords("button_press_event", ax, (100, 100), 1),
        MouseEvent._from_ax_coords("motion_notify_event", ax, (125, 125)),
        MouseEvent._from_ax_coords("button_release_event", ax, (125, 125), 1),
        KeyEvent("key_release_event", ax.figure.canvas, "control"),
        KeyEvent("key_press_event", ax.figure.canvas, "shift"),
        MouseEvent._from_ax_coords("motion_notify_event", ax, (100, 100)),
        MouseEvent._from_ax_coords("button_press_event", ax, (100, 100), 1),
        MouseEvent._from_ax_coords("motion_notify_event", ax, (125, 125)),
        MouseEvent._from_ax_coords("button_release_event", ax, (125, 125), 1),
        KeyEvent("key_release_event", ax.figure.canvas, "shift"),
        *polygon_place_vertex(ax, (50, 50)),
        *polygon_place_vertex(ax, (150, 50)),
        *polygon_place_vertex(ax, (50, 150)),
        *polygon_place_vertex(ax, (50, 50)),
    ]
    check_selector(event_sequence, expected_result, 1)

    # Try to place vertex out-of-bounds, then reset, and start a new polygon.
    expected_result = [(50, 50), (150, 50), (50, 150)]
    event_sequence = [
        *polygon_place_vertex(ax, (50, 50)),
        *polygon_place_vertex(ax, (250, 50)),
        KeyEvent("key_press_event", ax.figure.canvas, "escape"),
        KeyEvent("key_release_event", ax.figure.canvas, "escape"),
        *polygon_place_vertex(ax, (50, 50)),
        *polygon_place_vertex(ax, (150, 50)),
        *polygon_place_vertex(ax, (50, 150)),
        *polygon_place_vertex(ax, (50, 50)),
    ]
    check_selector(event_sequence, expected_result, 1)

