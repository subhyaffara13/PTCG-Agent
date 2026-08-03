import re

def as_euler(
    quat: Array, seq: str, degrees: bool = False, *, suppress_warnings: bool = False
) -> Array:
    xp = array_namespace(quat)

    # Sanitize the sequence
    if len(seq) != 3:
        raise ValueError(f"Expected 3 axes, got {seq}.")
    intrinsic = re.match(r"^[XYZ]{1,3}$", seq) is not None
    extrinsic = re.match(r"^[xyz]{1,3}$", seq) is not None
    if not (intrinsic or extrinsic):
        raise ValueError(
            "Expected axes from `seq` to be from ['x', 'y', 'z'] or ['X', 'Y', 'Z'], "
            f"got {seq}"
        )
    if any(seq[i] == seq[i + 1] for i in range(2)):
        raise ValueError(f"Expected consecutive axes to be different, got {seq}")

    device = xp_device(quat)
    axes = [_elementary_basis_index(x) for x in seq.lower()]
    axes = axes if extrinsic else axes[::-1]
    i, j, k = axes
    symmetric = i == k
    k = 3 - i - j if symmetric else k

    mask = xp.asarray(symmetric, device=device)
    sign = xp.asarray((i - j) * (j - k) * (k - i) // 2, dtype=quat.dtype, device=device)
    # Permute quaternion elements
    a = xp.where(mask, quat[..., 3], quat[..., 3] - quat[..., j])
    b = xp.where(mask, quat[..., i], quat[..., i] + quat[..., k] * sign)
    c = xp.where(mask, quat[..., j], quat[..., j] + quat[..., 3])
    d = xp.where(mask, quat[..., k] * sign, quat[..., k] * sign - quat[..., i])

    angles = _get_angles(
        extrinsic, symmetric, sign, xp.pi / 2, a, b, c, d, suppress_warnings
    )
    return _rad2deg(angles) if degrees else angles

