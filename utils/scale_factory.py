
def scale_factory(scale, axis, **kwargs):
    """
    Return a scale class by name.

    Parameters
    ----------
    scale : {%(names)s}
    axis : `~matplotlib.axis.Axis`
    """
    scale_cls = _api.getitem_checked(_scale_mapping, scale=scale)

    if _scale_has_axis_parameter[scale]:
        return scale_cls(axis, **kwargs)
    else:
        return scale_cls(**kwargs)

