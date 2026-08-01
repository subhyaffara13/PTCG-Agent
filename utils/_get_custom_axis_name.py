
def _get_custom_axis_name(axis: Dim | str) -> str:
    """Get the custom axis name from a torch.export.Dim."""
    if isinstance(axis, Dim):
        return axis.__name__
    return axis

