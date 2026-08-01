
def click_and_drag(tool, start, end, key=None):
    """
    Helper to simulate a mouse drag operation.

    Parameters
    ----------
    tool : `~matplotlib.widgets.Widget`
    start : [float, float]
        Starting point in data coordinates.
    end : [float, float]
        End point in data coordinates.
    key : None or str
         An optional key that is pressed during the whole operation
         (see also `.KeyEvent`).
    """
    ax = tool.ax
    if key is not None:  # Press key
        KeyEvent._from_ax_coords("key_press_event", ax, start, key)._process()
    # Click, move, and release mouse
    MouseEvent._from_ax_coords("button_press_event", ax, start, 1)._process()
    MouseEvent._from_ax_coords("motion_notify_event", ax, end, 1)._process()
    MouseEvent._from_ax_coords("button_release_event", ax, end, 1)._process()
    if key is not None:  # Release key
        KeyEvent._from_ax_coords("key_release_event", ax, end, key)._process()

