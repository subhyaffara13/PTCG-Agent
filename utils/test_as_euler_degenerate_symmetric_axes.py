
def test_as_euler_degenerate_symmetric_axes(
    xp, seq_tuple, intrinsic, suppress_warnings
):
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-6
    # Since we cannot check for angle equality, we check for rotation matrix
    # equality
    angles = xp.asarray([
        [15, 0, 60],
        [35, 0, 75],
        [60, 180, 35],
        [15, -180, 25]])

    # Rotation of the form A/B/A are rotation around symmetric axes
    seq = "".join([seq_tuple[0], seq_tuple[1], seq_tuple[0]])
    if intrinsic:
        # Extrinsic rotation (w.r.t. global world) at lower case
        # Intrinsic (WRT the object itself) upper case.
        seq = seq.upper()
    rotation = Rotation.from_euler(seq, angles, degrees=True)
    mat_expected = rotation.as_matrix()

    with maybe_warn_gimbal_lock(not suppress_warnings, xp):
        angle_estimates = rotation.as_euler(
            seq, degrees=True, suppress_warnings=suppress_warnings
        )
    mat_estimated = Rotation.from_euler(seq, angle_estimates, degrees=True).as_matrix()

    xp_assert_close(mat_expected, mat_estimated, atol=atol)

