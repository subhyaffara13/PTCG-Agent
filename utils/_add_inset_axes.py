
def _add_inset_axes(parent_axes, axes_class, axes_kwargs, axes_locator):
    """Helper function to add an inset axes and disable navigation in it."""
    if axes_class is None:
        axes_class = HostAxes
    if axes_kwargs is None:
        axes_kwargs = {}
    fig = parent_axes.get_figure(root=False)
    inset_axes = axes_class(
        fig, parent_axes.get_position(),
        **{"navigate": False, **axes_kwargs, "axes_locator": axes_locator})
    return fig.add_axes(inset_axes)

