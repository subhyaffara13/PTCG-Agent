
def _expand_footprint(ndim_image, axes, footprint,
                      footprint_name="footprint"):
    num_axes = len(axes)
    if num_axes < ndim_image:
        if footprint.ndim != num_axes:
            raise RuntimeError(f"{footprint_name}.ndim ({footprint.ndim}) "
                               f"must match len(axes) ({num_axes})")

        footprint = np.expand_dims(
            footprint,
            tuple(ax for ax in range(ndim_image) if ax not in axes)
        )
    return footprint

