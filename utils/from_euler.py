
def from_euler(seq: str, angles: Array, degrees: bool = False) -> Array:
    xp = array_namespace(angles)
    num_axes = len(seq)
    if num_axes < 1 or num_axes > 3:
        raise ValueError(
            "Expected axis specification to be a non-empty "
            f"string of up to 3 characters, got {seq}"
        )

    intrinsic = re.match(r"^[XYZ]{1,3}$", seq) is not None
    extrinsic = re.match(r"^[xyz]{1,3}$", seq) is not None
    if not (intrinsic or extrinsic):
        raise ValueError(
            "Expected axes from `seq` to be from ['x', 'y', "
            f"'z'] or ['X', 'Y', 'Z'], got {seq}"
        )

    if any(seq[i] == seq[i + 1] for i in range(num_axes - 1)):
        raise ValueError(f"Expected consecutive axes to be different, got {seq}")

    if degrees:
        angles = _deg2rad(angles)

    angles = xpx.atleast_nd(angles, ndim=1, xp=xp)

    if angles.shape[-1] != num_axes:
        raise ValueError(
            "Expected last dimension of `angles` to match number of sequence axes "
            f"specified, got {angles.shape[-1]}."
        )
    axes = [_elementary_basis_index(x) for x in seq.lower()]
    q = _elementary_quat_compose(axes, angles, intrinsic)
    return q

