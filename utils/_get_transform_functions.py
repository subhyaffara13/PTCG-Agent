
def _get_transform_functions(ax, axis):
    """Return the forward and inverse transforms for a given axis."""
    axis_obj = getattr(ax, f"{axis}axis")
    transform = axis_obj.get_transform()
    return transform.transform, transform.inverted().transform

