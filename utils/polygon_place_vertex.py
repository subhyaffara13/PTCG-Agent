
def polygon_place_vertex(ax, xy):
    return [
        MouseEvent._from_ax_coords("motion_notify_event", ax, xy),
        MouseEvent._from_ax_coords("button_press_event", ax, xy, 1),
        MouseEvent._from_ax_coords("button_release_event", ax, xy, 1),
    ]

