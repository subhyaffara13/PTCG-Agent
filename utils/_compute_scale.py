
def _compute_scale(in_size, out_size, align_corners, scale=None):
    if align_corners:
        return (in_size - 1.0) / (out_size - 1.0) if out_size > 1 else 0
    else:
        return 1.0 / scale if scale is not None and scale > 0 else in_size / out_size

