
def _zalpha(
    colors,
    zs,
    min_alpha=0.3,
    _data_scale=None,
):
    """Modify the alpha values of the color list according to z-depth."""

    if len(colors) == 0 or len(zs) == 0:
        return np.zeros((0, 4))

    # Alpha values beyond the range 0-1 inclusive make no sense, so clip them
    min_alpha = np.clip(min_alpha, 0, 1)

    if _data_scale is None or _data_scale == 0:
        # Don't scale the alpha values since we have no valid data scale for reference
        sats = np.ones_like(zs)

    else:
        # Deeper points have an increasingly transparent appearance
        sats = np.clip(1 - (zs - np.min(zs)) / _data_scale, min_alpha, 1)

    rgba = np.broadcast_to(mcolors.to_rgba_array(colors), (len(zs), 4))

    # Change the alpha values of the colors using the generated alpha multipliers
    return np.column_stack([rgba[:, :3], rgba[:, 3] * sats])

