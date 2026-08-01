
def _stale_figure_callback(self, val):
    if (fig := self.get_figure(root=False)) is not None:
        fig.stale = val

