
def as_davenport(
    quat: Array,
    axes: Array,
    order: str,
    degrees: bool = False,
    *,
    suppress_warnings: bool = False,
) -> Array:
    xp = array_namespace(quat)

    # Check argument validity
    if order in ["e", "extrinsic"]:
        extrinsic = True
    elif order in ["i", "intrinsic"]:
        extrinsic = False
    else:
        raise ValueError(
            "order should be 'e'/'extrinsic' for extrinsic sequences or 'i'/'intrinsic'"
            f" for intrinsic sequences, got {order}"
        )
    if axes.shape[-2] != 3:
        raise ValueError(f"Expected 3 axes, got {axes.shape}.")
    if axes.shape[-1] != 3:
        raise ValueError("Axes must be vectors of length 3.")
    if not broadcastable(axes.shape[:-2], quat.shape[:-1]):
        raise ValueError(
            f"Expected `axes` to match number of rotations, got {axes.shape} axes "
            f"and {quat.shape} rotations."
        )

    # normalize axes
    axes = axes / xp_vector_norm(axes, axis=-1, keepdims=True, xp=xp)
    vdot_ax0_ax1 = xp.vecdot(axes[..., 0, :], axes[..., 1, :])
    vdot_ax1_ax2 = xp.vecdot(axes[..., 1, :], axes[..., 2, :])
    is_invalid = (vdot_ax0_ax1 >= 1e-7) | (vdot_ax1_ax2 >= 1e-7)
    if is_lazy_array(is_invalid):
        axes = xp.where(is_invalid[..., None, None], xp.nan, axes)
    elif xp.any(is_invalid):
        raise ValueError("Consecutive axes must be orthogonal.")

    angles = _compute_davenport_from_quat(
        quat,
        axes[..., 0, :],
        axes[..., 1, :],
        axes[..., 2, :],
        extrinsic,
        suppress_warnings,
    )
    if degrees:
        angles = _rad2deg(angles)
    return angles

