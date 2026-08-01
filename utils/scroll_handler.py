
def scroll_handler(event, canvas=None, toolbar=None):
    ax = event.inaxes
    if ax is None:
        return
    if ax.name != "rectilinear":
        # zooming is currently only supported on rectilinear axes
        return

    if toolbar is None:
        toolbar = (canvas or event.canvas).toolbar

    if toolbar is None:
        # technically we do not need a toolbar, but until wheel zoom was
        # introduced, any interactive modification was only possible through
        # the toolbar tools. For now, we keep the restriction that a toolbar
        # is required for interactive navigation.
        return

    if event.key in {"control", "x", "y"}:  # zoom towards the mouse position
        toolbar.push_current()

        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        (xmin, ymin), (xmax, ymax) = ax.transScale.transform(
            [(xmin, ymin), (xmax, ymax)])

        # mouse position in scaled (e.g., log) data coordinates
        x, y = ax.transScale.transform((event.xdata, event.ydata))

        scale_factor = 0.85 ** event.step
        # Determine which axes to scale based on key
        zoom_x = event.key in {"control", "x"}
        zoom_y = event.key in {"control", "y"}

        if zoom_x:
            new_xmin = x - (x - xmin) * scale_factor
            new_xmax = x + (xmax - x) * scale_factor
        else:
            new_xmin, new_xmax = xmin, xmax

        if zoom_y:
            new_ymin = y - (y - ymin) * scale_factor
            new_ymax = y + (ymax - y) * scale_factor
        else:
            new_ymin, new_ymax = ymin, ymax

        inv_scale = ax.transScale.inverted()
        (new_xmin, new_ymin), (new_xmax, new_ymax) = inv_scale.transform(
            [(new_xmin, new_ymin), (new_xmax, new_ymax)])

        ax.set_xlim(new_xmin, new_xmax)
        ax.set_ylim(new_ymin, new_ymax)

        ax.figure.canvas.draw_idle()

