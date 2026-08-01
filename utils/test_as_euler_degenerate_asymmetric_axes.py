
def test_as_euler_degenerate_asymmetric_axes(
    xp, seq_tuple, intrinsic, suppress_warnings
):
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-6
    # Since we cannot check for angle equality, we check for rotation matrix
    # equality
    angles = xp.asarray([
        [45, 90, 35],
        [35, -90, 20],
        [35, 90, 25],
        [25, -90, 15]])

    seq = "".join(seq_tuple)
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

