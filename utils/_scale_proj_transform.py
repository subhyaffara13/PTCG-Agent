
def _scale_proj_transform(xs, ys, zs, axes):
    """
    Apply scale transforms and project.

    Combines `_apply_scale_transforms` and `proj_transform` into a single
    call. Returns txs, tys, tzs.
    """
    xs, ys, zs = _apply_scale_transforms(xs, ys, zs, axes)
    return proj_transform(xs, ys, zs, axes.M)

