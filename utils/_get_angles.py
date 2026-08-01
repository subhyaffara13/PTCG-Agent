
def _get_angles(
    extrinsic: bool,
    symmetric: bool,
    sign: int,
    lamb: float,
    a: Array,
    b: Array,
    c: Array,
    d: Array,
    suppress_warnings: bool,
) -> Array:
    xp = array_namespace(a)
    device = xp_device(a)
    eps = 1e-7
    half_sum = xp.atan2(b, a)
    half_diff = xp.atan2(d, c)
    # We zero-initialize to automatically cover singular cases where the second angle is
    # not defined uniquely.
    angles = xp.zeros((*a.shape, 3), dtype=a.dtype, device=device)

    angles = xpx.at(angles)[..., 1].set(2 * xp.atan2(xp.hypot(c, d), xp.hypot(a, b)))

    angle_first = 0 if extrinsic else 2
    angle_third = 2 if extrinsic else 0

    # Check if the second angle is close to 0 or pi, causing a singularity.
    # - Case 0: Second angle is neither close to 0 nor pi.
    # - Case 1: Second angle is close to 0.
    # - Case 2: Second angle is close to pi.
    case1 = xp.abs(angles[..., 1]) <= eps
    case2 = xp.abs(angles[..., 1] - xp.pi) <= eps
    case0 = ~(case1 | case2)
    if not suppress_warnings and not is_lazy_array(case0) and xp.any(~case0):
        warnings.warn(
            "Gimbal lock detected. Setting third angle to zero "
            "since it is not possible to uniquely determine "
            "all angles.",
            stacklevel=3,
        )

    # This writes case1 into a0 where True and case2 everywhere else. This is sound
    # because we later overwrite any values without singularity with the regular value
    # of case0. The second angle is covered by default since we zero-initialized the
    # second dimension.
    a0 = xp.where(case1, 2 * half_sum, 2 * half_diff * (-1 if extrinsic else 1))
    angles = xpx.at(angles)[..., 0].set(a0)

    # We overwrite the values of angles without singularities (case0)
    a1 = xp.where(case0, half_sum - half_diff, angles[..., angle_first])
    angles = xpx.at(angles)[..., angle_first].set(a1)

    # Same as above but for the third angle. We overwrite the non-singular case0 values
    a3 = xp.where(case0, half_sum + half_diff, angles[..., angle_third])
    if not symmetric:
        a3 = a3 * sign
        angles = xpx.at(angles)[..., 1].set(angles[..., 1] - lamb)
    angles = xpx.at(angles)[..., angle_third].set(a3)

    angles = (angles + xp.pi) % (2 * xp.pi) - xp.pi
    return angles

