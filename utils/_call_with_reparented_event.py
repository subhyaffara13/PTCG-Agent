
def _call_with_reparented_event(func):
    """
    Event callback decorator ensuring that the callback is called with an event
    that has been reparented to the widget's axes.
    """
    # This decorator handles the possibility that event.inaxes != self.ax
    # (e.g. if multiple Axes are overlaid), in which case event.xdata/.ydata
    # will be wrong.  Note that we still special-case the common case where
    # event.inaxes == self.ax and avoid re-running the inverse data transform,
    # because that can introduce floating point errors for synthetic events.
    @functools.wraps(func)
    def wrapper(self, event):
        if event.inaxes is not self.ax:
            event = copy.copy(event)
            event.guiEvent = None
            event.inaxes = self.ax
            try:
                event.xdata, event.ydata = (
                    self.ax.transData.inverted().transform((event.x, event.y)))
            except ValueError:  # cf LocationEvent._set_inaxes.
                event.xdata = event.ydata = None
        return func(self, event)

    return wrapper

