
def from_davenport(
    axes: Array, order: str, angles: Array, degrees: bool = False
) -> Array:
    xp = array_namespace(axes)
    device = xp_device(axes)
    if order in ["e", "extrinsic"]:  # Must be static, cannot be jitted
        extrinsic = True
    elif order in ["i", "intrinsic"]:
        extrinsic = False
    else:
        raise ValueError(
            "order should be 'e'/'extrinsic' for extrinsic sequences or 'i'/"
            f"'intrinsic' for intrinsic sequences, got {order}"
        )

    if axes.shape[-1] != 3:
        raise ValueError("Axes must be vectors of length 3.")

    axes = xpx.atleast_nd(axes, ndim=2, xp=xp)
    angles = xpx.atleast_nd(angles, ndim=1, xp=xp) 
    num_axes = axes.shape[-2]
    if num_axes < 1 or num_axes > 3:
        raise ValueError(f"Expected up to 3 axes, got {num_axes}")

    axes = axes / xp_vector_norm(axes, axis=-1, keepdims=True, xp=xp)

    # Check if axes are orthogonal. Shape checks also work for lazy backends.
    axes_not_orthogonal = xp.zeros(axes.shape[:-2], dtype=xp.bool, device=device)
    if num_axes > 1:
        # Cannot be True yet, so we do not need to use xp.logical_or
        axes_not_orthogonal = axes_not_orthogonal | (
            xp.abs(xp.vecdot(axes[..., 0, :], axes[..., 1, :])) > 1e-7
        )
    if num_axes > 2:
        axes_not_orthogonal = axes_not_orthogonal | (
            xp.abs(xp.vecdot(axes[..., 1, :], axes[..., 2, :])) > 1e-7
        )
    if not is_lazy_array(axes_not_orthogonal) and xp.any(axes_not_orthogonal):
        raise ValueError("Consecutive axes must be orthogonal.")
    else:
        axes = xp.where(axes_not_orthogonal[..., None, None], xp.nan, axes)

    if degrees:
        angles = _deg2rad(angles)

    if (
        not broadcastable(axes.shape[:-1], angles.shape)
        or axes.shape[-2] != angles.shape[-1]
    ):
        raise ValueError(
            f"Expected `angles` to match number of axes, got {angles.shape} angles "
            f"and {axes.shape} axes."
        )

    q_shape = angles.shape[:-1] + (4,)
    q = xp.zeros(q_shape, dtype=angles.dtype, device=xp_device(angles))
    q = xpx.at(q)[..., 3].set(1)

    for i in range(num_axes):
        qi = from_rotvec(angles[..., i, None] * axes[..., i, :])
        q = compose_quat(qi, q) if extrinsic else compose_quat(q, qi)
    return q

