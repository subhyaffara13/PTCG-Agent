
def _compute_davenport_from_quat(
    quat: Array,
    n1: Array,
    n2: Array,
    n3: Array,
    extrinsic: bool,
    suppress_warnings: bool,
) -> Array:
    # The algorithm assumes extrinsic frame transformations. The algorithm
    # in the paper is formulated for rotation quaternions, which are stored
    # directly by Rotation.
    # Adapt the algorithm for our case by reversing both axis sequence and
    # angles for intrinsic rotations when needed
    xp = array_namespace(quat)
    n1, n3 = (n1, n3) if extrinsic else (n3, n1)

    n_cross = xp.linalg.cross(n1, n2)
    lamb = xp.atan2(xp.vecdot(n3, n_cross), xp.vecdot(n3, n1))

    # alternative set of angles compatible with as_euler implementation
    mask = lamb < 0
    n2 = xp.where(mask[..., None], -n2, n2)
    lamb = xp.where(mask, -lamb, lamb)
    n_cross = xp.where(mask[..., None], -n_cross, n_cross)
    correct_set = mask

    quat_lamb = xp.concat(
        (xp.sin(lamb / 2)[..., None] * n2, xp.cos(lamb / 2)[..., None]), axis=-1
    )

    q_trans = compose_quat(quat_lamb, quat)
    a = q_trans[..., 3]
    b = xp.linalg.vecdot(q_trans[..., :3], n1)
    c = xp.linalg.vecdot(q_trans[..., :3], n2)
    d = xp.linalg.vecdot(q_trans[..., :3], n_cross)

    angles = _get_angles(extrinsic, False, 1, lamb, a, b, c, d, suppress_warnings)
    angles = xpx.at(angles)[..., 1].set(
        xp.where(correct_set, -angles[..., 1], angles[..., 1])
    )

    return angles

