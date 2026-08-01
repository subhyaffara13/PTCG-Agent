
def _scale_proj_transform_clip(xs, ys, zs, axes):
    """
    Apply scale transforms, project, and return clipping result.

    Returns txs, tys, tzs, tis.
    """
    xs, ys, zs = _apply_scale_transforms(xs, ys, zs, axes)
    vec = _vec_pad_ones(xs, ys, zs)
    return _proj_transform_vec_clip(vec, axes.M, axes._focal_length)

