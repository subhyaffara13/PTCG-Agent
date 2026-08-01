
def _mouse_handler(event):
    # Dead-reckoning of button and key.
    if event.name == "button_press_event":
        event.canvas._button = event.button
    elif event.name == "button_release_event":
        event.canvas._button = None
    elif event.name == "motion_notify_event" and event.button is None:
        event.button = event.canvas._button
    if event.key is None:
        event.key = event.canvas._key
    # Emit axes_enter/axes_leave.
    if event.name == "motion_notify_event":
        last_ref = LocationEvent._last_axes_ref
        last_axes = last_ref() if last_ref else None
        if last_axes != event.inaxes:
            if last_axes is not None:
                # Create a synthetic LocationEvent for the axes_leave_event.
                # Its inaxes attribute needs to be manually set (because the
                # cursor is actually *out* of that Axes at that point); this is
                # done with the internal _set_inaxes method which ensures that
                # the xdata and ydata attributes are also correct.
                try:
                    canvas = last_axes.get_figure(root=True).canvas
                    leave_event = LocationEvent(
                        "axes_leave_event", canvas,
                        event.x, event.y, event.guiEvent,
                        modifiers=event.modifiers)
                    leave_event._set_inaxes(last_axes)
                    canvas.callbacks.process("axes_leave_event", leave_event)
                except Exception:
                    pass  # The last canvas may already have been torn down.
            if event.inaxes is not None:
                event.canvas.callbacks.process("axes_enter_event", event)
        LocationEvent._last_axes_ref = (
            weakref.ref(event.inaxes) if event.inaxes else None)

