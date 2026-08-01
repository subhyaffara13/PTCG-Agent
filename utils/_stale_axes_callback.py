
def _stale_axes_callback(self, val):
    if self.axes:
        self.axes.stale = val

