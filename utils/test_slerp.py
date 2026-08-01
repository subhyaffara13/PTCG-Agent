
def test_slerp(xp):
    rnd = np.random.RandomState(0)

    key_rots = Rotation.from_quat(xp.asarray(rnd.uniform(size=(5, 4))))
    key_quats = key_rots.as_quat()

    key_times = [0, 1, 2, 3, 4]
    interpolator = Slerp(key_times, key_rots)
    assert isinstance(interpolator.times, type(xp.asarray(0)))

    times = [0, 0.5, 0.25, 1, 1.5, 2, 2.75, 3, 3.25, 3.60, 4]
    interp_rots = interpolator(times)
    interp_quats = interp_rots.as_quat()

    # Dot products are affected by sign of quaternions
    mask = (interp_quats[:, -1] < 0)[:, None]
    interp_quats = xp.where(mask, -interp_quats, interp_quats)
    # Checking for quaternion equality, perform same operation
    mask = (key_quats[:, -1] < 0)[:, None]
    key_quats = xp.where(mask, -key_quats, key_quats)

    # Equality at keyframes, including both endpoints
    xp_assert_close(interp_quats[0, ...], key_quats[0, ...])
    xp_assert_close(interp_quats[3, ...], key_quats[1, ...])
    xp_assert_close(interp_quats[5, ...], key_quats[2, ...])
    xp_assert_close(interp_quats[7, ...], key_quats[3, ...])
    xp_assert_close(interp_quats[10, ...], key_quats[4, ...])

    # Constant angular velocity between keyframes. Check by equating
    # cos(theta) between quaternion pairs with equal time difference.
    cos_theta1 = xp.sum(interp_quats[0, ...] * interp_quats[2, ...])
    cos_theta2 = xp.sum(interp_quats[2, ...] * interp_quats[1, ...])
    xp_assert_close(cos_theta1, cos_theta2)

    cos_theta4 = xp.sum(interp_quats[3, ...] * interp_quats[4, ...])
    cos_theta5 = xp.sum(interp_quats[4, ...] * interp_quats[5, ...])
    xp_assert_close(cos_theta4, cos_theta5)

    # theta1: 0 -> 0.25, theta3 : 0.5 -> 1
    # Use double angle formula for double the time difference
    cos_theta3 = xp.sum(interp_quats[1, ...] * interp_quats[3, ...])
    xp_assert_close(cos_theta3, 2 * (cos_theta1**2) - 1)

    # Miscellaneous checks
    assert_equal(len(interp_rots), len(times))

